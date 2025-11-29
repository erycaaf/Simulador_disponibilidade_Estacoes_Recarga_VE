import json
import os
import random
from src.simulated_station import SimulatedStation

# Variável global para armazenar as estações
stations_db = []  # type: list[SimulatedStation]

# Lista de status possíveis (Baseado no padrão Open Charge Map)
POSSIBLE_STATUSES = [
    {"ID": 10, "Title": "Available"},      # Disponível
    {"ID": 50, "Title": "Operational"},    # Operacional
    {"ID": 75, "Title": "Charging"},       # Carregando
    {"ID": 100, "Title": "Out of Service"}  # Fora de serviço
]


def load_data():
    """Lê o arquivo JSON e carrega na memória como SimulatedStation."""
    global stations_db

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, '../data/dados_estacoes_br.json')
    # --------------------------------------------------------

    if not os.path.exists(file_path):
        print("ERRO: Arquivo não encontrado!")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_stations = json.load(f)
            stations_db = [
                SimulatedStation.from_dict(st) for st in raw_stations]
        print(f"Sucesso! {len(stations_db)} estações carregadas.")
    except Exception as e:
        print(f"Erro ao ler JSON: {e}")


def get_all_stations():
    return [st.to_dict() for st in stations_db]


def get_station_by_id(station_id: int):
    for station in stations_db:
        if station.id == station_id:
            return station.to_dict()
    return None


def simulate_status_change():
    """
    Escolhe uma estação aleatória e altera seu status.
    Retorna um dicionário com o log da mudança.
    """
    if not stations_db:
        return None

    target_station = random.choice(stations_db)
    new_status = random.choice([s["Title"] for s in POSSIBLE_STATUSES])
    old_status = target_station.status
    target_station.update_status(new_status)
    return {
        "id": target_station.id,
        "potencia": target_station.potencia,
        "old_status": old_status,
        "new_status": new_status,
        "updated_at": target_station.updated_at.isoformat()
    }


def get_stations_by_city(city_name: str):
    """
    Filtra as estações pelo nome da cidade (case insensitive).
    """
    results = []
    search_term = city_name.lower().strip()
    for station in stations_db:
        if station.city and search_term in station.city.lower():
            results.append(station.to_dict())
    return results


load_data()
