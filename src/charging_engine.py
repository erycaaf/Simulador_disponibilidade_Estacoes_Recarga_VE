import ctypes
import os
import platform

# Define o caminho base
BASE_DIR = os.path.dirname(__file__)

# Define o nome do arquivo dependendo do sistema operacional
if os.name == 'nt':  # Windows
    LIB_NAME = "calculator.dll"
else:  # Linux / Mac
    LIB_NAME = "calculator.so"

LIB_PATH = os.path.join(BASE_DIR, 'core_c', LIB_NAME)

# Tenta carregar a biblioteca C
c_lib = None
try:
    if os.path.exists(LIB_PATH):
        c_lib = ctypes.CDLL(LIB_PATH)
        # Configura os tipos de entrada e saída da função C
        c_lib.calculate_minutes.argtypes = [
            ctypes.c_double, ctypes.c_double, ctypes.c_double
        ]
        c_lib.calculate_minutes.restype = ctypes.c_double
        print(f"Motor de cálculo C carregado: {LIB_NAME}")
    else:
        print(f"Aviso: Biblioteca C não encontrada em {LIB_PATH}")
except Exception as e:
    print(f"Erro ao carregar motor C: {e}")


def calculate_charging_time(battery_kwh, current_percent, power_kw=22.0):
    """
    Calcula o tempo de recarga.
    Tenta usar C (mais rápido). Se falhar, usa Python (backup).
    """
    # 1. Validações básicas
    if current_percent >= 100:
        return 0.0
    
    if power_kw <= 0:
        return -1.0

    # 2. Tenta usar o motor C
    if c_lib:
        try:
            return c_lib.calculate_minutes(
                float(battery_kwh),
                float(current_percent),
                float(power_kw)
            )
        except Exception as e:
            print(f"Erro na execução do C: {e}")

    # 3. Fallback (Plano B): Cálculo em Python puro
    # Isso garante que o teste passe no GitHub Actions mesmo sem o .dll/.so
    print("Usando cálculo fallback em Python.")
    needed_kwh = battery_kwh * (1.0 - (current_percent / 100.0))
    hours_needed = needed_kwh / power_kw
    minutes_needed = hours_needed * 60.0
    
    return round(minutes_needed, 2)
