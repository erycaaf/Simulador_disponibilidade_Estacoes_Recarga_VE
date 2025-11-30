ifeq ($(OS),Windows_NT)
	EXT = dll
	CC = cl
	CFLAGS = /LD
	SRC = src/core_c/calculator.c
	TARGET = src/core_c/calculator.$(EXT)
	RM_CMD = del src\core_c\*.dll src\core_c\*.exp src\core_c\*.lib src\core_c\*.obj 2>NUL || exit 0
	
build:
	@echo "🔨 Compilando modulo C para $(EXT)..."
	$(CC) $(CFLAGS) $(SRC) /Fe:$(TARGET)
	@echo "✅ Build concluido: $(TARGET)"
else
	EXT = so
	CC = gcc
	CFLAGS = -shared -fPIC
	SRC = src/core_c/calculator.c
	TARGET = src/core_c/calculator.$(EXT)
	RM_CMD = rm -f src/core_c/*.so

build:
	@echo "🔨 Compilando modulo C para $(EXT)..."
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)
	@echo "✅ Build concluido: $(TARGET)"
endif

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
