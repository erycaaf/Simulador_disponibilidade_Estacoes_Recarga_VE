import ctypes
import os


# 1. Detectar o Sistema Operacional (Windows ou Linux/Mac)
if os.name == 'nt':
    LIB_NAME = "calculator.dll"
else:
    LIB_NAME = "calculator.so"

# 2. Encontrar o caminho da biblioteca
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(BASE_DIR, "core_c", LIB_NAME)

c_lib = None

# 3. Tentar carregar a biblioteca C
try:
    if os.path.exists(LIB_PATH):
        c_lib = ctypes.CDLL(LIB_PATH)

        # Configura os tipos (Input: 3 floats / Output: 1 float)
        c_lib.calculate_charging_time.argtypes = [
            ctypes.c_float, ctypes.c_float, ctypes.c_float
        ]
        c_lib.calculate_charging_time.restype = ctypes.c_float
        print(f"Modulo C carregado: {LIB_NAME}")
    else:
        print(f"Aviso: Biblioteca C nao encontrada em {LIB_PATH}")

except Exception as e:
    print(f"Erro ao carregar modulo C: {e}")
    c_lib = None


def calculate_charging_time(
        battery_kwh: float,
        current_percent: float,
        power_kw: float) -> float:
    """
    Calcula o tempo de recarga.
    Prioridade: Motor C (Rapido) -> Fallback: Python (Compativel)
    """
    # Validação básica
    if current_percent >= 100:
        return 0.0
    if power_kw <= 0:
        return -1.0

    # Tenta usar o C
    if c_lib:
        try:
            return c_lib.calculate_charging_time(
                battery_kwh, current_percent, power_kw)
        except Exception as e:
            print(f"Erro ao executar C: {e}")

    # --- FALLBACK (PLANO B) ---
    # Se o C falhar ou não existir, calcula em Python
    print("Usando calculo fallback em Python.")
    needed_kwh = battery_kwh * (1.0 - (current_percent / 100.0))
    hours_needed = needed_kwh / power_kw
    minutes_needed = hours_needed * 60.0

    return round(minutes_needed, 2)
