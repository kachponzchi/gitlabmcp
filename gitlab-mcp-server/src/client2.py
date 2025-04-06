import asyncio
import os
import requests  # Using requests for direct GitLab API calls
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# KEEPING ORIGINAL get_llms() EXACTLY AS PROVIDED
def get_llms(model_name: str="gpt-3.5-turbo"):
    """
    Helper function to get OpenAI model instance with necessary API key and endpoint.
    
    Args:
        model_name: The name of the model to use
        
    Returns:
        A configured ChatOpenAI instance
    """
    return ChatOpenAI(
        openai_api_key=os.getenv(
            "OPEN_ROUTER_API_KEY", 
            "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"
        ),
        openai_api_base=os.getenv(
            "OPEN_ROUTER_BASE_URL", 
            "https://openrouter.ai/api/v1/chat/completions"
        ),
        model=model_name,
        temperature=0,
        base_url="https://openrouter.ai/api/v1",
        streaming=True
    )

async def handle_gitlab_operation(user_input: str):
    """Process common GitLab patterns with structured responses."""
    lower_input = user_input.lower()
    if "list" in lower_input and ("project" in lower_input or "repo" in lower_input):
        return {"action": "list_projects"}
    elif "issue" in lower_input and ("create" in lower_input or "add" in lower_input):
        return {"action": "create_issue", "details": user_input}
    return None

async def main():
    model = get_llms()

    gitlab_url = "http://192.168.100.68/api/v4"
    headers = {
        "PRIVATE-TOKEN": "REMOVED_SECRETVjd2-oma2m-SU39V_LBy",
        "Content-Type": "application/json"
    }

    print("\nGitLab MCP Client [type 'quit' to exit]")
    print("Try these commands:")
    print("- List my projects")
    print("- Create issue in project 1: Title='Bug' Description='Fix needed'")
    
    while True:
        user_input = input("\n> ").strip()
        if user_input.lower() in ('quit', 'exit'):
            break

        try:
            structured_query = await handle_gitlab_operation(user_input)
            
            if structured_query["action"] == "list_projects":
                response = requests.get(f"{gitlab_url}/projects", headers=headers)
                if response.status_code == 200:
                    print("\n" + "─" * 60)
                    print(response.json())
                    print("─" * 60)
                else:
                    print(f"⚠️ Error: {response.status_code} - {response.text}")
            elif structured_query["action"] == "create_issue":
                print("🚀 Issue creation feature not implemented yet")
            else:
                print("⚠️ Unknown command")

        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Common fixes:")
            print("- Check your command syntax")
            print("- Verify GitLab instance is accessible")
            print("- Ensure your token has 'api' scope")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSession ended by user")
