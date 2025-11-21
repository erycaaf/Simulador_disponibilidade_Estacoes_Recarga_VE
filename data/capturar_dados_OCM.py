import requests
import json

# --- Configurações ---

# URL base da API (sem os parâmetros)
BASE_URL = "https://api.openchargemap.io/v3/poi/"

API_KEY = "931185bb-a70c-4c8e-9771-0848d58de364" 

# Parâmetros da nossa busca
params = {
    'output': 'json',
    'countrycode': 'BR',
    'maxresults': 10000,
    'key': API_KEY  # A chave é adicionada aqui como um parâmetro da requisição
}

# Nome do arquivo onde os dados serão salvos
OUTPUT_FILENAME = "dados_estacoes_br.json"

# --- Início do Script ---

print("Iniciando a captura de dados da Open Charge Map...")

# Validação simples para garantir que a chave foi inserida
if "SUA_CHAVE" in API_KEY:
    print("\nERRO: Você esqueceu de colar sua chave de API na variável 'API_KEY' no script.")
    # Encerra o script se a chave não foi alterada
    exit()

try:
    print("Buscando dados da API com a sua chave...")
    # Faz a requisição passando a URL base e os parâmetros separadamente
    response = requests.get(BASE_URL, params=params, timeout=15)

    # Verifica se a requisição falhou
    response.raise_for_status()

    print("Dados recebidos com sucesso!")

    stations_data = response.json()
    print(f"Total de {len(stations_data)} estações de recarga encontradas.")

    print(f"Salvando os dados no arquivo '{OUTPUT_FILENAME}'...")
    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(stations_data, f, indent=4, ensure_ascii=False)

    print("\nProcesso concluído com sucesso!")
    print(f"Abra o arquivo '{OUTPUT_FILENAME}' para visualizar os dados.")

except requests.exceptions.HTTPError as http_err:
    print(f"\nERRO: Ocorreu um erro HTTP: {http_err}")
    print(f"Código de Status: {response.status_code}")
    if response.status_code == 403:
        print("Causa Provável: Sua chave de API pode ser inválida ou ter sido digitada incorretamente. Verifique a chave no script.")
    print(f"Resposta Completa: {response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"\nERRO: Ocorreu um erro na requisição (verifique sua conexão): {req_err}")
except Exception as err:
    print(f"\nERRO: Ocorreu um erro inesperado: {err}")
