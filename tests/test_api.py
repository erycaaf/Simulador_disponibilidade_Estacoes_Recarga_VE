import sys
import os
import pytest
from fastapi.testclient import TestClient

# --- Configuração de Caminhos ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.main import app

client = TestClient(app)

# --- Fixture: Uma função ajudante que roda antes dos testes ---
@pytest.fixture
def real_station_id():
    """
    Esta função pergunta à API quais estações existem
    e retorna o ID da primeira que encontrar.
    """
    response = client.get("/stations")
    if response.status_code == 200:
        stations = response.json()
        if stations and isinstance(stations, list) and len(stations) > 0:
            # Retorna o ID da primeira estação da lista (seja ele 1, 99 ou 5043)
            return stations[0].get("ID")
    return None

# --- Testes Unitários ---

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "total_stations" in response.json()

def test_list_all_stations():
    response = client.get("/stations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_station_existing(real_station_id):
    """Usa o ID real descoberto pela fixture."""
    if real_station_id is None:
        pytest.skip("Nenhuma estação encontrada no banco de dados para testar.")

    print(f"\n[DEBUG] Testando com o ID Real: {real_station_id}")
    
    response = client.get(f"/stations/{real_station_id}")
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se o ID retornado é o mesmo que pedimos
    # (converte para string ou int para garantir a comparação)
    assert str(data.get("ID")) == str(real_station_id)

def test_read_station_not_found():
    """Testa um ID absurdo que com certeza não existe."""
    response = client.get("/stations/99999999")
    assert response.status_code == 200 
    assert response.json() == {"error": "Station not found"}

def test_calculate_charge(real_station_id):
    """Usa o ID real para testar o cálculo."""
    if real_station_id is None:
        pytest.skip("Sem estação para calcular.")

    # Testa o cálculo na estação real
    response = client.get(f"/stations/{real_station_id}/calculate?battery_kwh=60&current_percent=20")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "estimated_minutes_remaining" in data
    assert data["estimated_minutes_remaining"] > 0
