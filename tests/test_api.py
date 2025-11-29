import sys
import os
import pytest
from fastapi.testclient import TestClient

# --- Configuração de Caminhos 
# Adiciona a pasta 'src' ao caminho do Python para conseguir importar o main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import app

# Instanciamos o cliente uma vez para ser usado em todos os testes
client = TestClient(app)

# --- Testes Unitários ---

def test_health_endpoint():
    """Testa se a API está viva."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_read_root():
    """Testa a rota raiz e verifica as informações básicas."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Simulador Ativo"
    # Verifica se o campo total_stations existe e é um número
    assert "total_stations" in data
    assert isinstance(data["total_stations"], int)

def test_list_all_stations():
    """Testa se a rota /stations retorna uma lista."""
    response = client.get("/stations")
    assert response.status_code == 200
    stations = response.json()
    assert isinstance(stations, list)
    # Se houver estações, verifica se a primeira tem um ID
    if len(stations) > 0:
        assert "ID" in stations[0]

def test_read_station_existing():
    """Testa a busca por um ID específico (Assumindo que ID 1 existe)."""
    response = client.get("/stations/1")
    
    # Se o banco de dados estiver vazio, pode retornar erro, então tratamos isso:
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 1
    else:
        # Se retornar erro, verificamos se é o erro esperado
        assert response.json() == {"error": "Station not found"}

def test_read_station_not_found():
    """Testa a busca por um ID que sabemos que não existe."""
    response = client.get("/stations/999999")
    # O seu código atual retorna 200 com mensagem de erro (o ideal seria 404, mas testamos o comportamento atual)
    assert response.status_code == 200 
    assert response.json() == {"error": "Station not found"}

def test_calculate_charge():
    """
    Testa o endpoint de cálculo.
    Verifica se a API aceita os parâmetros e devolve a estimativa.
    """
    # Simula: Bateria 60kWh, Carga atual 20%
    response = client.get("/stations/1/calculate?battery_kwh=60&current_percent=20")
    
    # Se a estação 1 não existir, o teste falha ou retorna erro, precisamos prever
    if response.json().get("error") == "Station not found":
        pytest.skip("Estação 1 não encontrada para teste de cálculo")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se o cálculo foi devolvido
    assert "estimated_minutes_remaining" in data
    assert isinstance(data["estimated_minutes_remaining"], (int, float))
