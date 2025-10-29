from typing import Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph
from pydantic import ValidationError

from state import State 
from utils import load_llm

def call_llm(state: State) -> State:
    result = load_llm().invoke(state["messages"])
    return {"messages": [result]}

def build_graph() -> CompiledStateGraph[State, None, State, State]:
    builder = StateGraph(State)

    builder.add_node("call_llm", call_llm)
    builder.add_edge(START, "call_llm")
    builder.add_edge("call_llm", END)

    return builder.compile(checkpointer=InMemorySaver())