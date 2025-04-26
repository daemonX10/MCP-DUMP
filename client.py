import asyncio
from dotenv import load_dotenv

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

from mcp_use import MCPAgent,MCPClient
import os

async def run_memory_chat():
    """Run a memory chat with the MCP agent"""
    load_dotenv()
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyD-59eZM0Yz5QeIV7bQabVzbtJjghWR-j4'
    
    config_file = "./weather.json"
    
    print("Starting MCP agent...")
    
    client = MCPClient.from_config_file(config_file)
    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash',temperature=0.2,google_api_key=os.environ['GOOGLE_API_KEY'])
    
    agent = MCPAgent(
        llm = llm,
        client= client,
        max_steps=15,
        memory_enabled=True,
        verbose=True
    )
    
    print("\n ========= Interactive MCP Chat =========")
    print(" Type 'exit' to end the conversation.")
    print(" Type 'clear' to clear the memory.")
    print(" Type 'help' to show this message.")
    print(" Type 'memory' to show the memory.")
    print(" ______________________________________")
    
    try:
        while True:
            #Get user input
            user_input = input("You: ")
            
            #check for exit command
            if user_input.lower() == 'exit':
                print("Exiting chat...")
                break
            
            #check for clear command
            if user_input.lower() == 'clear':
                agent.memory.clear()
                print("Memory cleared.")
                continue
            
            # get response from agent
            print("\n Assistant: ", end="",flush=True)
            
            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                print(traceback.format_exc())
    finally:
        #clean up
        if client and client.sessions:
            await client.close_all_sessions()
            
if __name__ == "__main__":
    asyncio.run(run_memory_chat())
        
