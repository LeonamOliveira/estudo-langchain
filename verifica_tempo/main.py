#Prompt
from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent, Context

app = FastAPI(
    title="Weather Pun API",
    description="An API that provides weather information with a punny twist.", 
    version="1.0.0"
)

class PerguntaClima(BaseModel):
    question: str
    user_id: str

@app.get("/healthcheck")
def health_check():
    return {"status": "Ok"}

@app.post("/verifica_tempo/")
def verifica_tempo(payload: PerguntaClima):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": payload.question}]},
        config={"configurable": {"thread_id": payload.user_id}},
        context=Context(user_id=payload.user_id)
    )
    return response['structured_response']
