from langchain_core.messages import HumanMessage
from agents import agent_app

def main():
    print("--- 🌩️ WEATHER AGENT (RTX 2050 EDITION) ---")
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        events = agent_app.stream(initial_state, stream_mode="values")
        
        for event in events:
            if "messages" in event:
                last_msg = event["messages"][-1]
                if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                     print(f"   Using Tool: {last_msg.tool_calls[0]['name']}...")
                elif last_msg.content and last_msg.type == "ai":
                     print(f"\nAgent: {last_msg.content}")

if __name__ == "__main__":
    main()