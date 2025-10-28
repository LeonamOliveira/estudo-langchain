from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextoRequest(BaseModel):
    texto: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_health():
    return {"status": "OK"}


@app.post("/processar_texto")
def process_text(req: TextoRequest):
    return {"texto_recebido": req.texto, "tamanho": len(req.texto), "prompt_para_llm"}


agent = create_agent(
    model=""
    system_prompt="Você é um agente que verifica o feedback dos clientes. Você deverá retornar se o feedback é positivo, negativo ou neutro."
)

agent.invoke(
    {
        "messages": [{"role": "user", "content":}]
    }
)