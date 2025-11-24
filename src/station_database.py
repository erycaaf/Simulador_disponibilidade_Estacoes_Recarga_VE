import json
import os
import random
from datetime import datetime

# Variável global para armazenar as estações
stations_db = []

# Lista de status possíveis (Baseado no padrão Open Charge Map)
POSSIBLE_STATUSES = [
    {"ID": 10, "Title": "Available"},      # Disponível
    {"ID": 50, "Title": "Operational"},    # Operacional
    {"ID": 75, "Title": "Charging"},       # Carregando
    {"ID": 100, "Title": "Out of Service"} # Fora de serviço
]

def load_data():
    """Lê o arquivo JSON e carrega na memória."""
    global stations_db
    file_path = "data/dados_estacoes_br.json"
    
    if not os.path.exists(file_path):
        print("ERRO: Arquivo não encontrado!")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            stations_db = json.load(f)
        print(f"Sucesso! {len(stations_db)} estações carregadas.")
    except Exception as e:
        print(f"Erro ao ler JSON: {e}")

def get_all_stations():
    return stations_db

def get_station_by_id(station_id: int):
    for station in stations_db:
        if station.get("ID") == station_id:
            return station
    return None

def simulate_status_change():
    """
    Escolhe uma estação aleatória e altera seu status.
    Retorna um dicionário com o log da mudança.
    """
    if not stations_db:
        return None

    # 1. Escolhe uma estação aleatória
    target_station = random.choice(stations_db)
    
    # 2. Escolhe um novo status aleatório
    new_status = random.choice(POSSIBLE_STATUSES)
    
    # 3. Pega o status antigo para mostrar no log
    # (Usa .get para evitar erro se o campo não existir)
    old_status_title = target_station.get('StatusType', {}).get('Title', 'Unknown')
    
    # 4. Atualiza a estação na memória
    target_station['StatusType'] = new_status
    target_station['DateLastStatusUpdate'] = datetime.utcnow().isoformat() + "Z"
    
    return {
        "id": target_station['ID'],
        "title": target_station.get('AddressInfo', {}).get('Title', 'No Title'),
        "old_status": old_status_title,
        "new_status": new_status['Title']
    }
<<<<<<< HEAD



def get_stations_by_city(city_name: str):
    """
    Filtra as estações pelo nome da cidade (case insensitive).
    """
    results = []
    search_term = city_name.lower().strip() # Transforma em minúsculo para facilitar a busca

    for station in stations_db:
        # Navega até o campo Town dentro de AddressInfo
        address = station.get('AddressInfo', {})
        town = address.get('Town')

        # Se a cidade existir e o termo buscado estiver nela
        if town and search_term in town.lower():
            results.append(station)
            
    return results

=======
>>>>>>> origin/dev
