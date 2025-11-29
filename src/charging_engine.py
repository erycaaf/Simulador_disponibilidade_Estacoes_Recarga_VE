import ctypes
import os
import platform  # Necessário para detectar se é Windows ou Linux

# 1. Detectar o Sistema Operacional para escolher a extensão correta
sistema = platform.system()

if sistema == "Windows":
    nome_arquivo = "calculator.dll"
else:
    # No Linux (Docker), bibliotecas compiladas usam .so
    nome_arquivo = "calculator.so"

# 2. Encontrar o caminho da biblioteca
# Pega o diretório onde este arquivo python está
base_dir = os.path.dirname(os.path.abspath(__file__))

# Monta o caminho completo: .../src/core_c/calculator.so (ou .dll)
lib_path = os.path.join(base_dir, "core_c", nome_arquivo)

# 3. Carregar a biblioteca C
try:
    c_lib = ctypes.CDLL(lib_path)

    # 4. Configurar os tipos de entrada e saída da função C
    # A função recebe 3 floats e retorna 1 float
    c_lib.calculate_charging_time.argtypes = [
        ctypes.c_float, ctypes.c_float, ctypes.c_float]
    c_lib.calculate_charging_time.restype = ctypes.c_float

    print(f"✅ Módulo C carregado com sucesso: {nome_arquivo}")

except Exception as e:
    print(f"❌ Erro ao carregar módulo C no caminho '{lib_path}': {e}")
    c_lib = None


def estimate_time(
        battery_kwh: float,
        current_percent: float,
        power_kw: float) -> float:
    """
    Chama a função em C para calcular o tempo restante em minutos.
    """
    if not c_lib:
        # Retorna erro ou valor padrão se a lib não carregou
        return -1.0

    # Chama a função compilada
    result = c_lib.calculate_charging_time(
        battery_kwh, current_percent, power_kw)
    return result
