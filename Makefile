# --- Variáveis de Configuração ---
CC = gcc
CFLAGS = -shared
SRC = src/core_c/calculator.c
TARGET = src/core_c/calculator.dll

# --- Regras (Targets) ---

# Regra padrão (roda quando você digita apenas 'make')
all: build

# Regra de Compilação
build:
	@echo "🔨 Compilando modulo C..."
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)
	@echo "✅ Build concluido: $(TARGET)"

# Regra para rodar a API (atalho)
run: build
	@echo "🚀 Iniciando servidor FastAPI..."
	uvicorn src.main:app --reload

# Regra de Limpeza (apaga a DLL para forçar recompilação)
clean:
	@echo "🧹 Limpando artefatos de build..."
	@if exist "src\core_c\calculator.dll" del "src\core_c\calculator.dll"
	@echo "✨ Limpeza concluida."

# Regra de Instalação de Dependências Python
install:
	pip install -r requirements.txt
