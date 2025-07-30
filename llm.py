# stock_agent/llm.py (Corrected for OpenRouter Best Practices)

import json
from groq import Groq
from openai import OpenAI

# Import our API keys securely from the config file
from config import GROQ_API_KEY, OPENROUTER_API_KEY

# --- Client Initialization ---

# 1. Groq Client (No changes needed)
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Failed to initialize Groq client: {e}")
    groq_client = None

# 2. OpenRouter Client (MODIFIED)
# We will now initialize it with default headers, as recommended by OpenRouter.
try:
    # Note the `default_headers` parameter which is the key change here.
    openrouter_client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        # ADDED: Default headers for every request sent via this client.
        # This aligns with the examples you provided.
        default_headers={
            "HTTP-Referer": "https://github.com/your-username/stock-agent", # Optional but recommended: Change to your project's URL
            "X-Title": "Stock Analyst Agent", # Optional but recommended: Change to your project's name
        },
    )
except Exception as e:
    print(f"Failed to initialize OpenRouter client: {e}")
    openrouter_client = None


def call_llm(client, model: str, messages: list, tools: list = None, tool_choice: str = "auto"):
    """
    A unified function to make calls to either Groq or OpenRouter.
    (This function's internal logic does not need to change).
    """
    if not client:
        raise ValueError("The specified LLM client is not initialized.")

    try:
        # The .chat.completions.create method will now automatically use the
        # default_headers we configured during client initialization.
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response.choices[0].message
    except Exception as e:
        # We print the error message more clearly now.
        print(f"An error occurred while calling the LLM API: {e}")
        return None