import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src import station_database

# --- Loop da Simulação ---
async def run_simulation():
    """Função que roda em paralelo enquanto a API estiver ligada."""
    print("⚡ Simulador Iniciado: Alterando status das estações...")
    while True:
        # Espera 5 segundos
        await asyncio.sleep(5)
        
        # Executa uma mudança de status
        change_log = station_database.simulate_status_change()
        
        if change_log:
            print(f"🔄 [SIMULAÇÃO] Estação {change_log['id']} mudou: "
                  f"{change_log['old_status']} -> {change_log['new_status']}")

# --- Configuração de Ciclo de Vida ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Carrega os dados ao iniciar
    station_database.load_data()
    
    # 2. Inicia a simulação em segundo plano
    simulation_task = asyncio.create_task(run_simulation())
    
    yield # A API fica rodando aqui
    
    # 3. Ao desligar, cancela a simulação
    simulation_task.cancel()

app = FastAPI(
    title="Simulador de Estações de Recarga",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {
        "message": "Simulador Ativo", 
        "total_stations": len(station_database.stations_db),
        "simulation_interval": "5 seconds"
    }

@app.get("/stations")
def list_all_stations():
    return station_database.get_all_stations()

@app.get("/stations/{station_id}")
def read_station(station_id: int):
    station = station_database.get_station_by_id(station_id)
    if station:
        return station
    return {"error": "Station not found"}
