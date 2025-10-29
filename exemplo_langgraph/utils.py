from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_openai import ChatOpenAI

def load_llm() -> BaseChatModel:
    return init_chat_model(model="gpt-4o-mini")