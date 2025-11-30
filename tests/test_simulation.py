import sys
import os
from unittest.mock import patch
import pytest
from src.station_database import SimulatedStation
# Configura o caminho para importar o código fonte
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import station_database

# --- Dados Falsos para Teste (Mock Data) ---
FAKE_STATION = SimulatedStation(
    id=999,
    potencia=50.0,
    status="Available",
    city="Estação Teste",
    created_at=None,
    updated_at=None
)

FAKE_NEW_STATUS = "Charging"


def test_simulation_empty_database():
    """
    Testa se a simulação lida bem quando não há estações.
    Deve retornar None e não quebrar.
    """
    # 'patch.object' substitui temporariamente a lista stations_db por uma lista vazia
    with patch.object(station_database, 'stations_db', []):
        result = station_database.simulate_status_change()
        assert result is None


def test_simulation_status_change():
    """
    Testa se a simulação realmente altera o status da estação.
    Aqui nós 'forçamos' o random a escolher nossa estação falsa.
    """
    # Criamos uma cópia para não sujar a global
    fake_db = [FAKE_STATION.copy()]

    # 1. Mockamos o banco de dados (stations_db) para usar nossa lista falsa
    with patch.object(station_database, 'stations_db', fake_db):
        # 2. Mockamos o random.choice
        # O side_effect define o que ele retorna a cada chamada:
        # 1ª chamada: Escolhe a estação
        # 2ª chamada: Escolhe o novo status (agora string)
        with patch('random.choice', side_effect=[fake_db[0], FAKE_NEW_STATUS]):
            # Executa a função
            log = station_database.simulate_status_change()

            # --- Validações ---
            # 1. O retorno do log está correto?
            assert log is not None
            assert log['id'] == 999
            assert log['old_status'] == "Available"
            assert log['new_status'] == "Charging"

            # 2. O objeto no banco de dados foi realmente atualizado?
            updated_station = fake_db[0]
            assert updated_station.status == "Charging"
            # Verifica se a data foi atualizada
            assert updated_station.updated_at != "2023-01-01T00:00:00Z"