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
            # Retorna o ID da primeira estação da lista
            return stations[0].get("ID")
    return None


# --- Testes Unitários Gerais ---

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

    response = client.get(f"/stations/{real_station_id}")
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se o ID retornado é o mesmo que pedimos
    assert str(data.get("ID")) == str(real_station_id)


def test_read_station_not_found():
    """Testa um ID absurdo que com certeza não existe."""
    response = client.get("/stations/99999999")
    assert response.status_code == 200
    assert response.json() == {"error": "Station not found"}


# --- Novos Testes de Cálculo de Carga (Incrementados) ---

def test_calculate_charge_success(real_station_id):
    """
    CAMINHO FELIZ:
    Testa um cenário normal. Bateria 60kWh, carga atual 20%.
    O resultado deve ser um número maior que zero.
    """
    if real_station_id is None:
        pytest.skip("Sem estação para calcular.")

    # Envia parâmetros válidos
    response = client.get(
        f"/stations/{real_station_id}/calculate?battery_kwh=60&current_percent=20"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Valida se os dados voltaram certos
    assert data["battery_kwh"] == 60.0
    assert data["current_percent"] == 20.0
    
    # Verifica se o tempo calculado é lógico (> 0)
    assert "estimated_minutes_remaining" in data
    assert data["estimated_minutes_remaining"] > 0


def test_calculate_charge_full_battery(real_station_id):
    """
    CASO DE BORDA:
    Se a bateria já está em 100%, o tempo restante deve ser 0.
    """
    if real_station_id is None:
        pytest.skip("Sem estação para calcular.")

    # Envia current_percent=100
    response = client.get(
        f"/stations/{real_station_id}/calculate?battery_kwh=60&current_percent=100"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Tempo deve ser exatamente zero
    assert data["estimated_minutes_remaining"] == 0.0


def test_calculate_invalid_input(real_station_id):
    """
    VALIDAÇÃO DE ERRO:
    Se enviar texto ('cem') em vez de número, a API deve retornar erro 422.
    """
    if real_station_id is None:
        pytest.skip("Sem estação para calcular.")

    # Tenta quebrar a API enviando texto no lugar de número
    response = client.get(
        f"/stations/{real_station_id}/calculate?battery_kwh=cem&current_percent=20"
    )
    
    # FastAPI valida tipos automaticamente e retorna 422 (Unprocessable Entity)
    assert response.status_code == 422
