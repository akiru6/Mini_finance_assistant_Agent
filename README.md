# Mini Finance Assistant Agent

Welcome to the Mini Finance Assistant Agent, a powerful command-line tool designed to provide real-time financial data, news sentiment, and economic indicators for stocks in both international and Chinese markets.

This agent is built to be modular and extensible, leveraging multiple APIs to deliver comprehensive financial insights. It uses a Large Language Model (LLM) to understand user queries, decide which tools to use, and synthesize the gathered information into a clear and concise answer.

## Features

- **Multi-API Data Integration**: Fetches data from a wide range of sources:
    - **Yahoo Finance**: For real-time international stock prices, market cap, and analyst recommendations.
    - **Alpha Vantage**: For in-depth fundamental company data.
    - **NewsAPI**: For top-tier financial news from sources like Bloomberg and Reuters.
    - **Tavily AI**: For advanced web searches on market sentiment and public opinion.
    - **AkShare**: For specific news related to Chinese A-share stocks.
    - **FRED**: For key US economic indicators like inflation and GDP.
- **Flexible LLM Backend**: Easily switch between different LLM providers:
    - **Groq**: For high-speed responses.
    - **OpenRouter**: For access to a variety of models, including those from Google and Moonshot AI.
- **Intelligent Tool Use**: The agent analyzes your question and automatically calls one or more tools in parallel to gather the necessary information.
- **Interactive CLI**: A user-friendly command-line interface built with `rich` for formatted, easy-to-read output.

## Project Structure

```
Mini_finance_assistant_Agent/
│
├── .env                # (You will create this) Your secret API keys
├── .env.sample         # Example environment file
├── requirements.txt    # Project dependencies
├── main.py             # Main entry point for the CLI application
├── agent.py            # Core agent logic for managing the conversation
├── llm.py              # Handles communication with LLM APIs (Groq, OpenRouter)
├── tools.py            # Defines all the data-gathering tools (APIs)
└── config.py           # Loads and validates API keys from the .env file
```

## Setup and Installation

Follow these steps to get the agent running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/akiru6/Mini_finance_assistant_Agent.git
cd Mini_finance_assistant_Agent
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

The agent requires API keys from several services.

1.  **Copy the sample environment file:**

    ```bash
    cp .env.sample .env
    ```

2.  **Edit the `.env` file** and add your own API keys. You can obtain them from the links below:
    *   [GROQ_API_KEY](https://console.groq.com/keys)
    *   [OPENROUTER_API_KEY](https://openrouter.ai/keys)
    *   [TAVILY_API_KEY](https://tavily.com/get-api-key)
    *   [ALPHA_VANTAGE_API_KEY](https://www.alphavantage.co/support/#api-key)
    *   [NEWSAPI_KEY](https://newsapi.org/)
    *   [FRED_API_KEY](https://fred.stlouisfed.org/docs/api/api_key.html)

### 5. Run the Agent

You are now ready to start the agent!

```bash
python main.py
```

You will be greeted by the welcome message and a prompt to ask your first question.

## How to Use

Simply type your financial question into the prompt and press Enter.

### Examples:

*   **Simple Query**: `What is the stock price and market cap of TSLA?`
*   **News Sentiment**: `What is the latest news sentiment for NVIDIA?`
*   **Complex Comparison**: `Compare the market cap of GOOGL and MSFT and tell me the latest news about both.`
*   **China Market Query**: `What is the latest news for Kweichow Moutai (600519)?`
*   **Economic Data**: `What is the current US unemployment rate?`

To end your session, simply type `quit` or `exit`.

## Switching LLM Models

You can easily change the LLM provider or model by editing the `agent.py` file.

Find this section in `agent.py`:

```python
# --- Model and Client Selection ---

# To use Groq:
# ACTIVE_CLIENT = groq_client
# MODEL = "moonshotai/kimi-k2-instruct"

# To use OpenRouter:
ACTIVE_CLIENT = openrouter_client
MODEL = "moonshotai/kimi-k2"
# MODEL = "google/gemini-flash-1.5"
```

Uncomment the client and model you wish to use. The agent will use your selected configuration for its next conversation.
```

---

#### 修正后的 `README.md` (中文版)

```markdown
# 财经小助理 (Mini Finance Assistant Agent)

欢迎使用财经小助理，这是一个功能强大的命令行工具，旨在为国际和中国市场的股票提供实时的金融数据、新闻情绪分析和关键经济指标。

该代理采用模块化和可扩展的设计，通过集成多个专业的API来提供全面、深入的金融见解。它利用大语言模型（LLM）来理解用户的自然语言查询，智能地决定调用一个或多个工具，并将收集到的信息整合成一份清晰、简洁的分析报告。

## 主要功能

- **多API数据集成**: 从广泛的专业数据源获取信息：
  - **Yahoo Finance**: 用于获取国际股票的实时价格、市值和分析师建议。
  - **Alpha Vantage**: 用于获取公司的深度基本面数据。
  - **NewsAPI**: 用于从彭博社、路透社等顶级来源获取财经新闻。
  - **Tavily AI**: 用于进行高级网络搜索，分析市场情绪和公众舆论。
  - **AkShare**: 用于获取中国A股市场的特定新闻。
  - **FRED**: 用于获取美国关键经济指标，如通货膨胀率（CPI）和国内生产总值（GDP）。
- **灵活的LLM后端**: 可轻松在不同的LLM供应商之间切换：
  - **Groq**: 提供极快的响应速度。
  - **OpenRouter**: 可访问包括Google、Moonshot AI等在内的多种模型。
- **智能工具调用**: 代理会分析您的问题，并自动并行调用一个或多个工具来收集所需信息。
- **交互式命令行界面**: 使用 `rich` 库构建了用户友好的命令行界面，输出格式清晰、易于阅读。

## 项目结构

```
Mini_finance_assistant_Agent/
│
├── .env                # (需要您自己创建) 存放您的API密钥
├── .env.sample         # 环境变量示例文件
├── requirements.txt    # 项目Python依赖
├── main.py             # CLI应用的主入口文件
├── agent.py            # 管理对话的核心代理逻辑
├── llm.py              # 处理与LLM API (Groq, OpenRouter) 的通信
├── tools.py            # 定义所有数据收集工具 (API)
└── config.py           # 从.env文件加载并验证API密钥
```

## 安装与设置

请按照以下步骤在您的本地计算机上安装并运行财经小助理。

### 第一步：克隆仓库

```bash
git clone https://github.com/akiru6/Mini_finance_assistant_Agent.git
cd Mini_finance_assistant_Agent
```

### 第二步：创建并激活虚拟环境

强烈建议使用虚拟环境来管理项目依赖，避免包版本冲突。

```bash
# 适用于 macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 适用于 Windows
python -m venv venv
.\venv\Scripts\activate
```

### 第三步：安装依赖

使用 `requirements.txt` 文件安装所有必需的Python库。

```bash
pip install -r requirements.txt
```

### 第四步：配置API密钥

此代理需要多个服务的API密钥才能正常工作。

1.  **复制环境变量示例文件：**

    ```bash
    cp .env.sample .env
    ```

2.  **编辑 `.env` 文件**，并填入您自己的API密钥。您可以从以下链接免费获取：
    *   [GROQ_API_KEY](https://console.groq.com/keys)
    *   [OPENROUTER_API_KEY](https://openrouter.ai/keys)
    *   [TAVILY_API_KEY](https://tavily.com/get-api-key)
    *   [ALPHA_VANTAGE_API_KEY](https://www.alphavantage.co/support/#api-key)
    *   [NEWSAPI_KEY](https://newsapi.org/)
    *   [FRED_API_KEY](https://fred.stlouisfed.org/docs/api/api_key.html)

### 第五步：运行代理

现在您可以启动代理程序了！

```bash
python main.py
```

您将看到欢迎信息和提问输入提示。

## 如何使用

只需在提示符后输入您的财经问题，然后按回车键即可。

### 使用示例:

*   **简单查询**: `What is the stock price and market cap of TSLA?` (查询TSLA的股价和市值)
*   **新闻情绪分析**: `What is the latest news sentiment for NVIDIA?` (NVIDIA最近的新闻情绪如何？)
*   **复杂对比查询**: `Compare the market cap of GOOGL and MSFT and tell me the latest news about both.` (对比GOOGL和MSFT的市值，并告诉我它们俩的最新消息。)
*   **中国市场查询**: `What is the latest news for Kweichow Moutai (600519)?` (贵州茅台（600519）有什么最新消息？)
*   **经济数据查询**: `What is the current US unemployment rate?` (当前美国的失业率是多少？)

要结束会话，只需输入 `quit` 或 `exit`。

## 切换LLM模型

您可以非常轻松地更改代理使用的LLM供应商或具体模型。

在 `agent.py` 文件中找到以下部分：

```python
# --- Model and Client Selection ---

# 如需使用 Groq:
# ACTIVE_CLIENT = groq_client
# MODEL = "moonshotai/kimi-k2-instruct"

# 如需使用 OpenRouter:
ACTIVE_CLIENT = openrouter_client
MODEL = "moonshotai/kimi-k2"
# MODEL = "google/gemini-flash-1.5"
```

只需取消注释您希望使用的 `ACTIVE_CLIENT` 和 `MODEL`，然后重新运行程序即可。代理将在下一次对话中使用您的新配置。
```
