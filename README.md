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

---

## ✨ Funcionalidades

* **Integração com Dados Reais:** Consome APIs públicas (como a Open Charge Map) para obter a localização e características técnicas de estações de recarga verdadeiras, usando-as como base para a simulação.
* **Simulação de Estado em Tempo Real:** Gerencia o ciclo de vida de cada estação, permitindo que seu status seja alterado entre 'Disponível', 'Ocupado' ou 'Em Recarga' através de chamadas de API.
* **Cálculo de Recarga de Bateria:** Simula a evolução da carga da bateria de um veículo durante o processo de recarga, utilizando um motor de cálculo otimizado para performance.
* **Interação via API REST:** Expõe todos os dados e funcionalidades através de endpoints claros, permitindo que sistemas externos consultem o status das estações ou interajam com a simulação.
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
