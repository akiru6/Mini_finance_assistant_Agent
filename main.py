# stock_agent/main.py

from rich.console import Console
from rich.markdown import Markdown

# Import our new conversation runner function
from agent import run_conversation

# Initialize a rich Console for beautiful terminal output
console = Console()


def main():
    """
    The main function to run the command-line interface.
    """
    welcome_message = """
Welcome to the **Stock Analyst Agent v2** (Manual Control)!
You can ask me for financial data or recent news about stocks.
- Try: `What is the stock price and market cap of TSLA?`
- Or: `What is the latest news sentiment for NVIDIA?`
- Or a complex one: `Compare the market cap of GOOGL and MSFT and tell me the latest news about both.`
Type `quit` or `exit` to end the session.
    """
    console.print(Markdown(welcome_message))

    while True:
        # Prompt the user for input
        query = console.input("\n[bold yellow]Your question:[/bold yellow] ")

        # Check for exit command
        if query.lower() in ["quit", "exit"]:
            console.print("[bold blue]Goodbye![/bold blue]")
            break
        
        # Run the conversation and get the final result
        final_result = run_conversation(query)
        
        # Use rich's Markdown for nicely formatted output
        console.print("\n[bold green]Assistant's Response:[/bold green]")
        console.print(Markdown(final_result))


if __name__ == "__main__":
    main()