FROM python:3.11-slim

# Evita lixo do Python e logs presos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o PYTHONPATH para achar a pasta src
ENV PYTHONPATH=/app

WORKDIR /app

# 1. Instala compiladores (GCC e Make) necessários para o código C
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia o código todo
COPY . .

# 4. Compila o código C para gerar o arquivo .so (Linux)
# O comando 'make' vai ler seu Makefile e criar o binário compatível
RUN make

# Expõe a porta 8000 (apenas documentação para quem lê)
EXPOSE 8000

# O comando REAL que inicia o servidor
# src.main:app significa -> arquivo src/main.py, variável 'app'
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

