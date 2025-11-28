import ctypes
import os

# 1. Encontrar o caminho da DLL
# Pega o diretório onde este arquivo python está
base_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(base_dir, "core_c", "calculator.dll")

# 2. Carregar a biblioteca C
try:
    c_lib = ctypes.CDLL(dll_path)

    # 3. Configurar os tipos de entrada e saída da função C
    # A função recebe 3 floats e retorna 1 float
    c_lib.calculate_charging_time.argtypes = [
        ctypes.c_float, ctypes.c_float, ctypes.c_float]
    c_lib.calculate_charging_time.restype = ctypes.c_float

    print("✅ Módulo C carregado com sucesso!")

except Exception as e:
    print(f"❌ Erro ao carregar módulo C: {e}")
    c_lib = None


def estimate_time(
        battery_kwh: float,
        current_percent: float,
        power_kw: float) -> float:
    """
    Chama a função em C para calcular o tempo restante em minutos.
    """
    if not c_lib:
        return -1.0

    # Chama a função compilada
    result = c_lib.calculate_charging_time(
        battery_kwh, current_percent, power_kw)
    return result
