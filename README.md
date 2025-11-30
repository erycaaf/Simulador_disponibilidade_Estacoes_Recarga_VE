# Simulador de Disponibilidade de Estações de Recarga

---

## 📄 Descrição

É um serviço de backend (API) projetado para simular o status em tempo real de uma rede de estações de recarga para veículos elétricos. O sistema combina dados geográficos reais de estações existentes com uma camada de simulação de estado (disponibilidade, uso, recarga), criando um ambiente realista para o desenvolvimento e teste de outras aplicações, como planejadores de rota ou sistemas de gerenciamento de frota.

---

## 👥 Equipe de Desenvolvimento

- **Eryca Francyele**
- **Renato Silva**
- **Rian Linhares**

Os papéis de desenvolvedor, testador e gerente de projeto são rotativos entre os membros da equipe.

---

## ⚙️ Requisitos do Projeto

- **Python:** 3.11.2
- **Dependências:** Listadas em `requirements.txt`

Se necessário, atualize o arquivo `requirements.txt` para garantir que todas as bibliotecas utilizadas estejam listadas corretamente.

---

## 🚀 Como Executar o Projeto

1. Instale as dependências:
	```bash
	python -m pip install -r requirements.txt
	```
2. Execute o serviço:
	```bash
	python -m src.main
	```

## 🐳 Executando com Docker
O projeto possui suporte completo a Docker, garantindo que o ambiente (incluindo a compilação do módulo em C para Linux) seja configurado automaticamente.

1. Construir a Imagem

Este comando lê o Dockerfile, instala as dependências, compila o código C (.so) e prepara a aplicação.

```bash
docker build -t 
simulador-disponibilidade .
```

2. Rodar o Container

Inicia o servidor web dentro do container e libera a porta 8000 para acesso local.

```bash
docker run --rm -p 8000:8000 simulador-disponibilidade
```
--rm: Remove o container automaticamente ao desligar (limpa o ambiente).

-p 8000:8000: Permite acessar a API pelo seu navegador.
Após rodar, a API estará disponível em:

Home: http://localhost:8000

Documentação Interativa (Swagger): http://localhost:8000/docs

## 🧪 Como Executar os Testes

Para rodar os testes automatizados, defina o PYTHONPATH para o diretório do projeto:

No PowerShell (Windows):
```powershell
$env:PYTHONPATH="."; pytest
```

No Bash (Linux/macOS):
```bash
PYTHONPATH=. pytest
```

---

## ⚡️ Integração Contínua (CI)

O projeto utiliza dois workflows principais no GitHub Actions:

- **Build e Lint:** Executado a cada push ou pull request. Realiza checkout do código, instala dependências, executa o lint (`flake8`) e roda os testes (`pytest`). O `PYTHONPATH` é configurado para o diretório raiz do projeto, garantindo que os imports funcionem corretamente no ambiente de CI.

- **Nightly:** Executado automaticamente todas as noites às 03:00 UTC. Além dos testes, gera relatórios de cobertura (`coverage.xml`) e logs do pytest, que são disponibilizados como artefatos para download e análise posterior.

### Exemplo de configuração do PYTHONPATH no workflow:
```yaml
env:
	PYTHONPATH: ${{ github.workspace }}
```

### Artefatos gerados no workflow noturno:
- `coverage.xml`: Relatório de cobertura dos testes
- `.pytest_cache`: Logs detalhados da execução dos testes

Consulte os arquivos `.github/workflows/build.yml` e `.github/workflows/nightly.yml` para detalhes e personalizações.

---

## ✨ Funcionalidades

* **Integração com Dados Reais:** Consome APIs públicas (como a Open Charge Map) para obter a localização e características técnicas de estações de recarga verdadeiras, usando-as como base para a simulação.
* **Simulação de Estado em Tempo Real:** Gerencia o ciclo de vida de cada estação, permitindo que seu status seja alterado entre 'Disponível', 'Ocupado' ou 'Em Recarga' através de chamadas de API.
* **Cálculo de Recarga de Bateria:** Simula a evolução da carga da bateria de um veículo durante o processo de recarga, utilizando um motor de cálculo otimizado para performance.
* **Interação via API REST:** Expõe todos os dados e funcionalidades através de endpoints claros, permitindo que sistemas externos consultem o status das estações ou interajam com a simulação.

### 🧩 Como funciona a simulação

* Cada estação é representada por um objeto Python (`SimulatedStation`).
* Se o valor de potência (`Potencia`) não estiver definido nos dados, ele será preenchido automaticamente com um valor aleatório escolhido de uma lista realista de potências de carregadores (ex: 7.2, 22, 50, 150, 300 kW, etc).
* O status inicial da estação (`Status`) também é preenchido aleatoriamente entre os valores possíveis: 'Available', 'Operational', 'Charging', 'Out of Service', caso não esteja presente nos dados.
* A cidade da estação é extraída do campo `AddressInfo['Town']` e pode ser usada para consultas, como filtrar todas as estações de uma cidade específica.
* Todos os atributos (potência, status, cidade, timestamps) podem ser acessados e atualizados durante a simulação, permitindo cenários dinâmicos e realistas.
## 🛠️ Comandos Makefile

O projeto inclui um `Makefile` para facilitar tarefas comuns de desenvolvimento. Você pode usar os comandos abaixo no terminal, na raiz do projeto:

### Compilar o módulo C
```bash
make build
```
Compila o arquivo `src/core_c/calculator.c` e gera `src/core_c/calculator.dll`.

### Rodar a API
```bash
make run
```
Compila o módulo C (se necessário) e inicia o servidor FastAPI com recarregamento automático.

### Instalar dependências Python
```bash
make install
```
Instala todas as dependências listadas em `requirements.txt`.

### Limpar artefatos de build
```bash
make clean
```
Remove o arquivo `calculator.dll` para forçar uma nova compilação.

---

## 📘 Documentação da API (Swagger)

A aplicação possui documentação interativa gerada automaticamente via **Swagger UI**.  
Essa interface permite visualizar endpoints, parâmetros, modelos de dados e executar requisições diretamente do navegador.

---

### Acessar o Swagger

Assim que o servidor estiver rodando, abra no navegador:

**Swagger UI**  
http://localhost:8000/docs

**Redoc (documentação alternativa)**  
http://localhost:8000/redoc

---

### Como usar

Na interface do Swagger, você pode:

- Visualizar todos os endpoints disponíveis
- Expandir cada rota para ver:
  - Método (GET, POST, etc.)
  - Descrição do endpoint
  - Parâmetros esperados
  - Exemplos de requisição
  - Exemplos de resposta
- Clicar em **“Try it out”** para:
  - Executar chamadas diretamente do navegador
  - Alterar valores de entrada
  - Ver o JSON retornado pela API em tempo real

---

### Esquema OpenAPI

Se quiser obter o esquema completo da API:

- No Swagger UI, clique em **“Download OpenAPI Specification”**,  
  **ou**
- Acesse diretamente:

➡️ http://localhost:8000/openapi.json

---


## 📝 Convenção de Commits

Este projeto segue o padrão **Conventional Commits** para manter um histórico organizado e facilitar automações.

**Formato:**
```
<tipo>(escopo opcional): descrição curta
```

**Tipos principais:**
* `feat` – nova funcionalidade
* `fix` – correção de bug
* `docs` – documentação
* `style` – formatação sem mudança de lógica
* `refactor` – refatoração sem alterar comportamento
* `test` – criação ou ajuste de testes
* `ci` – mudanças em pipelines (GitHub Actions)
* `chore` – tarefas gerais

**Exemplos:**
```
feat(api): adiciona endpoint de consulta de status
fix(simulator): corrige cálculo de disponibilidade
docs(readme): adiciona seção sobre convenção de commits
ci: cria workflow de testes automatizados
```
