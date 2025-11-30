# --- Detecção do Sistema Operacional ---
ifeq ($(OS),Windows_NT)
    # Configurações para Windows
    EXT = dll
    CFLAGS = -shared
    RM_CMD = del src\core_c\*.dll 2>NUL || exit 0
else
    # Configurações para Linux (Docker)
    EXT = so
    # -fPIC é obrigatório para Linux
    CFLAGS = -shared -fPIC
    RM_CMD = rm -f src/core_c/*.so
endif

# --- Variáveis de Configuração ---
CC = gcc
SRC = src/core_c/calculator.c
# O nome do arquivo final muda dinamicamente (.dll ou .so)
TARGET = src/core_c/calculator.$(EXT)

# --- Regras (Targets) ---

all: build

# Regra de Compilação
build:
	@echo "🔨 Compilando modulo C para $(EXT)..."
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)
	@echo "✅ Build concluido: $(TARGET)"

# Regra para rodar a API (atalho local)
run: build
	@echo "🚀 Iniciando servidor FastAPI..."
	uvicorn src.main:app --reload


# Regra para rodar os testes (garante build do C antes)
test: build
	@echo "🧪 Executando testes..."
	pytest

# Regra de Limpeza (Adaptada para o SO correto)
clean:
	@echo "🧹 Limpando artefatos de build..."
	-$(RM_CMD)
	@echo "✨ Limpeza concluida."

# Regra de Instalação
install:
	pip install -r requirements.txt
