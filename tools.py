# stock_agent/tools.py (Corrected and Finalized)

import json
import yfinance as yf
from tavily import TavilyClient
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# --- NEW IMPORTS FOR ADDITIONAL TOOLS ---
from alpha_vantage.fundamentaldata import FundamentalData
from newsapi import NewsApiClient
from fredapi import Fred
import akshare as ak # ADDED: Import AkShare for China market data


# Import all API keys from our secure config file
from config import (
    TAVILY_API_KEY, 
    ALPHA_VANTAGE_API_KEY, 
    NEWSAPI_KEY, 
    FRED_API_KEY
)

# Initialize the Tavily client once using our API key
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


# --- Pydantic Models for Structured Output ---
class StockInfo(BaseModel):
    """A model to hold key financial data for a stock."""
    ticker: str = Field(..., description="The stock ticker symbol.")
    current_price: float = Field(..., description="The current market price of the stock.")
    market_cap: int = Field(..., description="The total market capitalization of the company.")
    recommendation: str = Field(..., description="The consensus analyst recommendation (e.g., 'Buy', 'Hold').")
    currency: str = Field(..., description="The currency in which the financial data is reported.")


# --- Tool Function Definitions ---

def tavily_search(query: str) -> str:
    """
    Searches the web using Tavily for up-to-date information, news, and market sentiment.
    Use this for general questions, recent events, or public opinion.
    """
    print(f"\n--- Executing Tavily Search for: {query} ---")
    try:
        response = tavily_client.search(
            query=query, 
            search_depth="advanced",
            topic="general", 
            max_results=5
        )
        return json.dumps(response['results'])
    except Exception as e:
        return f"An error occurred during Tavily search: {e}"


def get_stock_financial_data(ticker: str) -> str:
    """
    Fetches key financial data for a stock ticker using Yahoo Finance.
    Use for quantitative data like price, market cap, and recommendations for international stocks.
    """
    print(f"\n--- Fetching Yahoo Finance Data for: {ticker} ---")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if 'currentPrice' not in info or info['currentPrice'] is None:
            raise ValueError(f"Invalid ticker symbol or no data available for '{ticker}'.")
        stock_info = StockInfo(
            ticker=ticker.upper(),
            current_price=info.get('currentPrice'),
            market_cap=info.get('marketCap', 0),
            recommendation=info.get('recommendationKey', 'N/A').capitalize(),
            currency=info.get('currency', 'USD')
        )
        return stock_info.model_dump_json()
    except Exception as e:
        return f"An error occurred while fetching stock data: {e}"

def get_company_overview(ticker: str) -> str:
    """
    Fetches detailed company overview (fundamental data) for a stock ticker using Alpha Vantage.
    Use for deep-dive questions about a company's business, sector, P/E ratio, etc.
    """
    print(f"\n--- Fetching Alpha Vantage Fundamental Data for: {ticker} ---")
    try:
        fd = FundamentalData(key=ALPHA_VANTAGE_API_KEY, output_format='json')
        data, _ = fd.get_company_overview(symbol=ticker)
        if not data:
            return f"No data found for ticker '{ticker}'. It might be an invalid symbol."
        return json.dumps(data)
    except Exception as e:
        return f"An error occurred while fetching from Alpha Vantage: {e}"

def get_specific_financial_news(query: str) -> str:
    """
    Fetches recent financial news about a topic from top-tier sources using NewsAPI.
    """
    print(f"\n--- Fetching Financial News from NewsAPI for: {query} ---")
    try:
        newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        top_headlines = newsapi.get_everything(
            q=query,
            sources='bloomberg,reuters,the-wall-street-journal,financial-post',
            language='en',
            sort_by='publishedAt',
            page_size=5
        )
        return json.dumps(top_headlines['articles'])
    except Exception as e:
        return f"An error occurred while fetching from NewsAPI: {e}"

def get_economic_indicator(series_id: str) -> str:
    """
    Fetches data for a specific US economic indicator from FRED.
    Common series IDs: 'CPIAUCSL' (Inflation), 'GDP' (GDP), 'UNRATE' (Unemployment Rate).
    """
    print(f"\n--- Fetching FRED Economic Data for Series: {series_id} ---")
    try:
        fred = Fred(api_key=FRED_API_KEY)
        recent_values = fred.get_series(series_id).tail(5)
        return recent_values.to_json(orient='index', date_format='iso')
    except Exception as e:
        return f"An error occurred while fetching from FRED API: {e}"

# tools.py 中需要被替换的函数

# tools.py 中需要被替换的函数 (最终修正版)

def get_china_stock_news(symbol: str) -> str:
    """
    Fetches recent news for a specific Chinese A-share stock using its symbol.
    Use this for news/sentiment on Chinese stocks. The symbol should be a 6-digit string, e.g., '600519' for Kweichow Moutai.
    """
    print(f"\n--- Fetching China A-Share News from AkShare for: {symbol} ---")
    try:
        # 1. 获取原始数据
        news_df = ak.stock_news_em(symbol=symbol)

        if news_df.empty:
            return f"No news found for China A-share stock symbol: {symbol}"
            
        # 2. [最终修正] 使用从调试日志中发现的、正确的【中文】列名
        expected_columns = ['发布时间', '新闻标题', '新闻链接']
        
        # 检查所有期望的中文列是否存在
        for col in expected_columns:
            if col not in news_df.columns:
                # 如果Akshare再次改变格式，这个检查依然能保护我们
                error_message = f"Data source for symbol {symbol} is missing the expected Chinese column '{col}'. Unable to process."
                print(f"[Error] {error_message}")
                return error_message

        # 3. [最终修正] 使用正确的中文列名进行数据处理
        top_5_news = news_df.head(5)
        
        # 选择我们需要的列
        top_5_news_filtered = top_5_news[expected_columns]
        
        # 为了让LLM更容易理解，我们将中文列名重命名为简洁的英文名
        rename_map = {
            '新闻标题': 'headline', 
            '发布时间': 'time',
            '新闻链接': 'url'
        }
        top_5_news_formatted = top_5_news_filtered.rename(columns=rename_map)
        
        # to_json现在是完全安全的
        return top_5_news_formatted.to_json(orient='records', force_ascii=False, date_format='iso')
        
    except Exception as e:
        # 捕获其他任何意外错误
        return f"An unexpected error occurred while fetching China stock news via AkShare: {e}"

# --- UPDATED Manual Tool Schema Generation ---
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": "Searches the web for up-to-date information, news, and market sentiment.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The search query, e.g., 'NVIDIA stock sentiment'."}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_financial_data",
            "description": "Fetches key financial data for an international stock ticker (e.g., US stocks).",
            "parameters": {
                "type": "object",
                "properties": {"ticker": {"type": "string", "description": "The stock ticker symbol, e.g., 'NVDA'."}},
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_overview",
            "description": "Fetches detailed company overview (fundamental data) for an international stock ticker.",
            "parameters": {
                "type": "object",
                "properties": {"ticker": {"type": "string", "description": "The stock ticker symbol, e.g., 'AAPL'."}},
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_specific_financial_news",
            "description": "Fetches recent financial news from top-tier international sources about a topic.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The search topic, e.g., 'NVIDIA AI chips'."}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_economic_indicator",
            "description": "Fetches data for a US economic indicator from FRED. Use IDs like 'CPIAUCSL', 'GDP', 'UNRATE'.",
            "parameters": {
                "type": "object",
                "properties": {"series_id": {"type": "string", "description": "The official series ID, e.g., 'CPIAUCSL'."}},
                "required": ["series_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_china_stock_news",
            "description": "Fetches recent news for a specific Chinese A-share stock using its symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The 6-digit stock symbol for a Chinese A-share company, e.g., '600519'."
                    }
                },
                "required": ["symbol"]
            }
        }
    }
]

# --- UPDATED Tool-to-Function Mapping ---
AVAILABLE_TOOLS = {
    "tavily_search": tavily_search,
    "get_stock_financial_data": get_stock_financial_data,
    "get_company_overview": get_company_overview,
    "get_specific_financial_news": get_specific_financial_news,
    "get_economic_indicator": get_economic_indicator,
    # FIXED: Added the missing mapping for your new tool
    "get_china_stock_news": get_china_stock_news,
}