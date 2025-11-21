from fastapi import FastAPI

app = FastAPI(
    title="Simulador de Estações de Recarga",
    description="API para simulação de status de carregadores de VEs",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "API do Simulador Online!", "status": "OK"}
