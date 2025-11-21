from fastapi import FastAPI
from contextlib import asynccontextmanager
from src import station_database

# O 'lifespan' define o que acontece quando a API liga e desliga
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Antes da API começar: Carrega os dados
    station_database.load_data()
    yield
    # Depois da API parar: (Nada por enquanto)

app = FastAPI(
    title="Simulador de Estações de Recarga",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {
        "message": "API Online", 
        "total_stations": len(station_database.stations_db),
        "docs_url": "/docs"
    }

@app.get("/stations")
def list_all_stations():
    """Retorna todas as estações carregadas."""
    return station_database.get_all_stations()

@app.get("/stations/{station_id}")
def read_station(station_id: int):
    """Busca uma estação específica pelo ID."""
    station = station_database.get_station_by_id(station_id)
    if station:
        return station
    return {"error": "Station not found"}
