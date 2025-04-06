import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI


import os
from langchain_openai import ChatOpenAI

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

async def main():
    model = get_llms()

    async with MultiServerMCPClient(
        {
            "github": {
                "url": "http://localhost:8080/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        
        while True:
            # Get user input
            user_input = input("\nEnter your message (or 'quit' to exit): ")
            
            # Check for quit condition
            if user_input.lower() == 'quit':
                break
            
            # Create the query
            query = {"messages": user_input}
            
            try:
                # Invoke agent and get response
                response = await agent.ainvoke(query)
                
                # Extract and print the AI's response
                messages = response.get('messages', [])
                for message in messages:
                    if hasattr(message, 'content'):
                        print("\nAI Response:")
                        print("-" * 50)
                        print(message.content)
                        print("-" * 50)
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    asyncio.run(main())