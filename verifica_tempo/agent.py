from dotenv import load_dotenv
from pydantic import BaseModel

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime

load_dotenv()

SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""

class Context(BaseModel):
    """Custom runtime context schema."""
    user_id: str

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

model = init_chat_model(
    model="gpt-4o-mini",
    temperature=0.8,
    timeout=10,
    max_tokens=1000
)

# We use a dataclass here, but Pydantic models are also supported.
class ResponseFormat(BaseModel):
    """Response schema for the agent."""
    punny_response: str
    weather_conditions: str | None = None

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}
