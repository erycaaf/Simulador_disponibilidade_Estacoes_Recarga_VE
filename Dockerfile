FROM python:3.11-slim

# Variáveis de ambiente para comportamento do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Define diretório de trabalho
WORKDIR /app

# Instala ferramentas de compilação para o módulo C (gcc, make, etc.)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# Compila o módulo C (.so para Linux)
RUN make

# Expõe a porta do FastAPI
EXPOSE 8000

# Inicia o backend FastAPI com Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

