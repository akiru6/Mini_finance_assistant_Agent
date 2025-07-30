# stock_agent/agent.py

import json
from rich.console import Console

# Import our custom LLM calling function
from llm import call_llm, groq_client, openrouter_client

# Import the tools and their definitions
from tools import AVAILABLE_TOOLS, TOOL_DEFINITIONS

# Initialize a console for pretty printing
console = Console()

# --- Model and Client Selection ---
# Define which client and model we want to use for the conversation.
# This makes it easy to switch between Groq and OpenRouter.


# ACTIVE_CLIENT = groq_client
# MODEL = "moonshotai/kimi-k2-instruct" 


# To use OpenRouter:
ACTIVE_CLIENT = openrouter_client
MODEL = "moonshotai/kimi-k2"
# MODEL = "google/gemini-2.0-flash-exp:free"


# --- Agent System Instructions ---
# These instructions are now part of the initial message to the LLM.
SYSTEM_PROMPT = """
You are a highly-skilled financial analyst assistant. Your main goal is to help users by providing insightful, data-driven analysis of stocks.

Here's your workflow:
1. When a user asks a question, analyze it to see if you need external data.
2. If you need information about recent events, public opinion, or news, decide to use the `tavily_search` tool.
3. If you need specific financial metrics (like stock price, market cap), decide to use the `get_stock_financial_data` tool.
4. You can and should call multiple tools if the user's question requires it.
5. Once you have the data from the tools, you will be called again to synthesize this information into a concise, easy-to-understand summary.
6. Always state the stock ticker symbol clearly in your final answer. Present financial data first, followed by a summary of news and sentiment.
7. Do not make up information. If you cannot find the information, state that clearly.
"""


def run_conversation(user_prompt: str):
    """
    Manages the main conversation loop for the agent.
    """
    # 1. Initialize the conversation history with the system prompt and the user's first message.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    
    console.print("\n[bold cyan]Thinking...", justify="left")

    # --- Main Loop: LLM decides, we execute ---
    while True:
        # 2. Call the LLM to get its next action (either a response or a tool call)
        response_message = call_llm(ACTIVE_CLIENT, MODEL, messages, TOOL_DEFINITIONS)

        if not response_message:
            return "Sorry, there was an error processing your request."

        # 3. Check if the LLM decided to call any tools.
        if response_message.tool_calls:
            # Append the assistant's decision to call tools to the history
            messages.append(response_message)
            
            # 4. Execute the tool calls.
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_to_call = AVAILABLE_TOOLS.get(function_name)
                
                if not function_to_call:
                    console.print(f"[bold red]Error: LLM tried to call unknown function '{function_name}'[/bold red]")
                    continue
                
                try:
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the actual Python function with the arguments
                    function_response = function_to_call(**function_args)
                    
                    # 5. Append the tool's output to the history for the LLM to see.
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                except Exception as e:
                    console.print(f"[bold red]Error executing tool '{function_name}': {e}[/bold red]")
            
            # Go back to the start of the loop to let the LLM process the tool results.
            console.print("[bold cyan]Got tool results, summarizing...", justify="left")
            continue 
        
        else:
            # 6. If no tool calls, the LLM has generated a final answer.
            # Return the content of the response and break the loop.
            return response_message.content