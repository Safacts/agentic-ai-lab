from typing import TypedDict, Annotated, List
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, BaseMessage
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from tools import available_tools

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# Localhost works on Windows too
llm = ChatOllama(base_url="http://localhost:11434", model="llama3.2", temperature=0)
llm_with_tools = llm.bind_tools(available_tools)

sys_msg = SystemMessage(content="You are a Weather Reporter. Always use the 'get_weather' tool when asked about weather.")

def assistant(state: AgentState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(available_tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
agent_app = builder.compile()