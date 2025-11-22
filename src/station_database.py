import json
import os


# Variável global para armazenar as estações em memória
stations_db = []

def load_data():
    """
    Lê o arquivo JSON local e carrega na memória.
    """
    global stations_db
    
    # Caminho relativo para o arquivo na pasta 'data'
    # Assumindo que estamos rodando o comando da raiz do projeto
    file_path = "data/dados_estacoes_br.json"
    
    print(f"Tentando carregar dados de: {file_path}")
    
    if not os.path.exists(file_path):
        print("ERRO CRÍTICO: Arquivo de dados não encontrado!")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            stations_db = json.load(f)
        print(f"Sucesso! {len(stations_db)} estações carregadas na memória.")
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")

def get_all_stations():
    return stations_db

def get_station_by_id(station_id: int):
    # Procura na lista uma estação que tenha esse ID
    for station in stations_db:
        if station.get("ID") == station_id:
            return station
    return None
