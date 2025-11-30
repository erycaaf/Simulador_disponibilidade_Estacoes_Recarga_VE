
# --- Windows: Use MinGW-w64 gcc for CI, cl for local MSVC builds ---
ifeq ($(OS),Windows_NT)
    EXT = dll
    SRC = src/core_c/calculator.c
    TARGET = src/core_c/calculator.$(EXT)
    RM_CMD = del src\core_c\*.dll 2>NUL || exit 0
    # Default to cl, override with CC=gcc for CI
    CC ?= cl
    ifeq ($(CC),cl)
        CFLAGS = /LD
        BUILD_CMD = $(CC) $(CFLAGS) $(SRC) /Fe:$(TARGET)
    else
        CFLAGS = -shared
        BUILD_CMD = $(CC) $(CFLAGS) -o $(TARGET) $(SRC)
    endif
else
    EXT = so
    CC = gcc
    CFLAGS = -shared -fPIC
    SRC = src/core_c/calculator.c
    TARGET = src/core_c/calculator.$(EXT)
    RM_CMD = rm -f src/core_c/*.so
    BUILD_CMD = $(CC) $(CFLAGS) -o $(TARGET) $(SRC)
endif

build:
	@echo "🔨 Compilando modulo C para $(EXT)..."
	$(BUILD_CMD)
	@echo "✅ Build concluido: $(TARGET)"

# --- Regras (Targets) ---

all: build

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
