# stock_agent/config.py (Updated to include Tushare)

import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root.
load_dotenv()

# --- API Key Configuration ---
# This section now loads all the keys our agent might need.

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

# # ADDED: Retrieve the Tushare Pro API Token for China stock data
# TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")


# --- Validation ---
# We now check for every key required by our tools.

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file. Please add it.")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set in the .env file. Please add it.")

if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("ALPHA_VANTAGE_API_KEY is not set in the .env file. Please add it.")

if not NEWSAPI_KEY:
    raise ValueError("NEWSAPI_KEY is not set in the .env file. Please add it.")

if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY is not set in the .env file. Please add it.")

# # ADDED: Validation for the new Tushare token
# if not TUSHARE_TOKEN:
#     raise ValueError("TUSHARE_TOKEN is not set in the .env file. Please add it.")