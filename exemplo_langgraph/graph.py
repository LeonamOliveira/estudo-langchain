from typing import Literal

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph
from pydantic import ValidationError

from state import State 
from tools import TOOLS, TOOLS_BY_NAME
from utils import load_llm

def call_llm(state: State) -> State:
    print('> call llm')
    llm_with_tools = load_llm().bind_tools(TOOLS)
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": [result]}

def tool_node(state: State) -> State:
    print('> tool node')
    llm_response = state['messages'][-1]

    if not isinstance(llm_response, AIMessage) and getattr(
        llm_response, "tool_calls", None
    ):
        return state
     
    call = llm_response.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]

    try: 
        content = TOOLS_BY_NAME[name].invoke(args)
        status = "success"
    except(KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
        content = f"Please, fix your mistakes: {error}"
        status = "error"

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)

    return {'messages': [tool_message]}            

def router(state: State) -> Literal['tool_node', '__end__']:
    print('> router')

    llm_response = state["messages"][-1]

    if isinstance(llm_response, AIMessage) and llm_response.tool_calls:
        print('> Router')
        return 'tool_node'

    return '__end__'

def build_graph() -> CompiledStateGraph[State, None, State, State]:
    builder = StateGraph(State)

    builder.add_node("call_llm", call_llm)
    builder.add_node("tool_node", tool_node)

    builder.add_edge(START, "call_llm")
    builder.add_conditional_edges('call_llm', router, ['tool_node', '__end__'])
    
    builder.add_edge("call_llm", END)

    return builder.compile(checkpointer=InMemorySaver())