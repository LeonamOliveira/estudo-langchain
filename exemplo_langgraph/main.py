from dotenv import load_dotenv
from graph import build_graph
from rich import print

from langchain_core.messages import HumanMessage
from langgraph.graph.state import RunnableConfig

load_dotenv()

def main() -> None:
    config = RunnableConfig(configurable={"thread_id": 1})
    graph = build_graph()

    user_input = "Me informa quanto é 1.13 * 3"
    human_message = HumanMessage(user_input)
    current_messages = [human_message]
    result = graph.invoke({"messages": current_messages}, config=config)

    print(result)

if __name__ == "__main__":
    main()