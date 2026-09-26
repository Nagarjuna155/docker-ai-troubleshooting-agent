import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

async def main():
    # this bring all the tools from docker_mcp server.py
    client = MultiServerMCPClient(
        { 
            "docker-mcp": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python",
                "args": ["docker_mcp_server.py"]
            }
        }
    )

    tools = await client.get_tools() # local tools or MCP tools
    # LLM
    llm = ChatOllama(
        model="gemma4:26b",
        temperature=0.8, # temperature controlls the randomness of response
    )
    agent = create_agent(
        llm,
        tools  
    )

    print("Docker MCP Assistant — ask about containers, logs, issues, or RCA.")
    print("Type 'exit' or 'quit' to stop.\n")

    # keep history so follow-ups have context (e.g. "why did it crash?")
    conversation = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("Goodbye.")
            break

        conversation.append({"role": "user", "content": user_input})

        try:
            response = await agent.ainvoke({"messages": conversation})
        except Exception as e:
            print(f"[Error while processing request: {e}]\n")
            continue

        ai_message = response["messages"][-1]
        print(f"\nAssistant: {ai_message.content}\n")

        # keep the full running message history for context in next turn
        conversation = response["messages"]


if __name__ == "__main__":
    asyncio.run(main())