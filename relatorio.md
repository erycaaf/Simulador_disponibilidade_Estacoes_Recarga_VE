# Relatório do Projeto — Simulador de Disponibilidade de Estações de Recarga de VE

📌 Introdução

Este documento apresenta a visão geral do projeto Simulador de Disponibilidade de Estações de Recarga de Veículos Elétricos, desenvolvido como parte da disciplina de Gerência de Configuração e Mudanças (SCM).

O foco principal foi demonstrar a aplicação prática de ferramentas e metodologias de SCM, contemplando versionamento, modelagem de branching, controle de mudanças, integração contínua, rastreabilidade, documentação, automação de build e empacotamento com Docker.

Além do desenvolvimento do software, o trabalho enfatizou a organização colaborativa do time, o registro das atividades no GitHub e a elaboração de artefatos essenciais para controle de configuração.

---
## 1. Escopo do Projeto
O projeto implementa uma API que simula a disponibilidade de estações de recarga de veículos elétricos. Entre suas principais funcionalidades, destacam-se:

* Consulta do status atual das estações (available, charging, etc);
* Simulação de eventos que alteram estados das estações;
* Cálculo de tempo e nível de recarga;
* Filtragem de estações por cidade;
* Comunicação com uma fonte externa (dados OCM);
* Documentação automática via Swagger;
* Execução via Docker;
* Testes integrados e pipeline contínuo;
* Interface web simples para visualização da simulação em tempo real.

A aplicação foi implementada majoritariamente em Python, com testes automatizados e suporte de execução padronizada via Docker. Além disso, parte da lógica de simulação também foi desenvolvida em C, utilizada para rotinas de processamento de estados e cálculos de atualização de eventos com maior desempenho (funcionalidade de cálculo de distribuição de carga e simulação de comportamento estatístico das estações). Esse módulo nativo, compilado via Makefile, foi integrado ao fluxo geral da aplicação para demonstrar práticas de SCM envolvendo múltiplas linguagens e processos de build distintos.

---
## 2. Organização da Equipe e Papéis Assumidos

A equipe é composta por três integrantes: Eryca, Renato e Rian. Conforme exigido, todos atuaram em pelo menos duas funções. Embora o projeto tenha seguido uma divisão por etapas, a colaboração foi contínua, e cada membro assumiu responsabilidades complementares.

| **Integrante** | **Funções exercidas** | **Exemplos de Atividades** |
|----------------|------------------------|-----------------------------|
| **Eryca** | Gerente de Configuração, Desenvolvedora, Build/CI | Organização de branches, revisão de PRs, criação de issues, labels, kanban (GitHub Projects), definição de versionamento e releases; Implementação de endpoints, cálculo de recarga, manutenção do pipeline CI. |
| **Renato** | Desenvolvedor, Testador, Build/CI | Implementação de módulos internos, endpoints, criação de testes, desenvolvimento de interface, validações de integração (GitHub Actions) e manutenção do pipeline de CI, revisão de PRs. |
| **Rian** | Desenvolvedor, Testador, Gerente de Configuração | Criação de estrutura base da API, implementação de endpoints, testes de build e unitários, correção de bugs e manutenção de ambiente (Docker), revisão de PRs e atualização de versão. |

---
## 3. Estratégia de Branching

O projeto adotou uma estratégia inspirada no Git Flow, simplificada para o contexto acadêmico. Assim, duas branches são principais e permanentes: `main` e `dev`. As demais branches são de suporte, necessárias para criação de funcionalidades e alterações específicas como descrito a seguir.
* `main` — versão estável
* `dev` — ambiente de integração em desenvolvimento
* `feat/` — branches para cada nova funcionalidade
* `ci/` — branches específicas para pipeline
* `docs/` — branches para documentação
* `fix/` — branches para correções pontuais
* `test/` — branches para testes

### Boas práticas aplicadas:

Cada feature iniciou sempre em sua própria branch.
Os PRs foram abertos para revisão antes do merge.
Os commits seguiram o padrão “conventional commits” da forma:
* `feat` – nova funcionalidade
* `fix` – correção de bug
* `docs` – documentação
* `style` – formatação sem mudança de lógica
* `refactor` – refatoração sem alterar comportamento
* `test` – criação ou ajuste de testes
* `ci` – mudanças em pipelines (GitHub Actions)
* `chore` – tarefas gerais

---

## 4. Controle de Mudanças e Rastreabilidade

O GitHub foi utilizado como plataforma central de gestão das mudanças. Foram criadas:

* Issues para cada tarefa, contendo descrição, responsáveis e labels. 
As labels utilizadas foram:
    * `enhancement`: utilizada para indicar novas funcionalidades, melhorias de comportamento ou adição de novas capacidades à aplicação.
    * `bug`: empregada para reportar falhas, comportamentos incorretos ou erros encontrados durante o uso ou testes da aplicação.
    * `documentation`: destinada a tarefas relacionadas à criação, atualização ou reorganização de documentação, incluindo README, Swagger, relatórios e instruções de uso.
    * `testing`: aplicada a atividades envolvendo criação, manutenção ou revisão de testes automatizados, validando o comportamento esperado do sistema.
    * `ci`: utilizada para atividades associadas à integração contínua, incluindo ajustes em pipelines, workflows do GitHub Actions ou scripts automáticos de build.
    * `config`: atribuída a tarefas de configuração do ambiente, ajustes no Dockerfile, docker-compose, Makefile ou outras dependências do projeto.

* Pull Requests com referências cruzadas para issues, utilizando closes #X, garantindo encerramento automático.
* Code reviews realizados por pelo menos um integrante antes da integração.
* Histórico documentado de versões e releases, com suas respectivas tags para identificar estados estáveis.

O fluxo utilizado:
1. Criar uma issue
2. Criar branch correspondente
3. Implementar a feature
4. Abrir PR
5. Revisão por outro membro
6. Merge em `dev`
7. Após conjunto de features → merge em `main`
8. Criação da tag (ex.: `v0.1.0`)

---
## 5. Processos de Build e Integração Contínua (CI/CD)

A automação foi estabelecida como um pilar fundamental para garantir a integridade do código e a agilidade nas entregas. Utilizamos o **GitHub Actions** para orquestrar o pipeline de CI/CD, assegurando que cada alteração submetida passasse por critérios rigorosos de qualidade antes de ser integrada à branch principal.

O workflow foi configurado para ser disparado automaticamente a cada *push* ou *pull request* direcionado às branches `main` e `dev`. O pipeline é composto pelos seguintes estágios sequenciais:

### 1. Preparação do Ambiente (Setup)
O pipeline é executado em containers Linux (`ubuntu-latest`). Esta etapa realiza o checkout do código e a configuração do ambiente Python, garantindo uma base limpa e isolada para cada execução.

### 2. Análise Estática (Linting)
Antes de qualquer execução lógica, o código passa pelo **Flake8**. Esta etapa atua como um *Quality Gate* inicial, verificando a conformidade com a PEP-8 e detectando erros de sintaxe, variáveis não utilizadas e problemas de formatação. Se o código não estiver dentro do padrão, o build falha imediatamente.

### 3. Build do Módulo Nativo (Compilação C)
Este é o estágio mais crítico da configuração. Como o projeto possui um motor de cálculo híbrido, o pipeline executa a compilação do código C utilizando o `gcc` para gerar a biblioteca compartilhada (`.so`) compatível com o ambiente Linux do CI.

*   **Desafio superado:** Enquanto o desenvolvimento local ocorria majoritariamente em Windows (gerando `.dll`), o CI validou a portabilidade do código ao compilar e executar com sucesso em Linux, demonstrando a robustez da configuração multiplataforma.

### 4. Testes Automatizados
Com o ambiente pronto e o módulo C compilado, o **Pytest** é acionado para executar a suíte de testes. O pipeline valida:

*   **Testes Unitários:** Verificação isolada dos endpoints da API.
*   **Testes de Integração:** Validação da comunicação entre o Python e a biblioteca C compilada.
*   **Testes com Mocks:** Simulação de cenários de borda e comportamento do banco de dados.

A implementação deste fluxo contínuo eliminou o problema de *"regressão silenciosa"* (bugs introduzidos por novas funcionalidades) e garantiu que a versão `main` estivesse sempre em um estado implantável (*deployable*).


---
## 6. Docker e Ambiente Reprodutível

Um dos maiores desafios em Gerência de Configuração é garantir a **consistência de ambientes** entre as máquinas dos desenvolvedores e o ambiente de produção/teste. Para mitigar o clássico problema "na minha máquina funciona", todo o ecossistema da aplicação foi containerizado utilizando **Docker**.

A estratégia de containerização foi decisiva para o sucesso do projeto, especialmente devido à arquitetura híbrida (Python + C). O `Dockerfile` foi estruturado para atuar não apenas como um empacotador, mas como um **ambiente de build padronizado**.

A construção da imagem segue as seguintes etapas (conforme implementado no arquivo final):

1. **Definição da Base:** Utilização da imagem oficial `python:3.11-slim`. A escolha da versão *slim* garantiu um container leve, contendo apenas o essencial para o sistema operacional Linux.
2. **Preparação para Compilação:** Instalação do pacote `build-essential`. Esta etapa é crítica, pois disponibiliza as ferramentas `gcc` e `make` dentro do container, permitindo a compilação de código nativo.
3. **Gerenciamento de Dependências:** Instalação das bibliotecas Python via `requirements.txt` e configuração de variáveis de ambiente (`PYTHONUNBUFFERED=1`) para garantir que os logs da aplicação sejam visualizados em tempo real.
4. **Build do Motor Híbrido:** Execução explícita do comando `RUN make`. Isso garante que a biblioteca C (`.so`) seja compilada **durante a construção da imagem**, garantindo que o binário seja compatível com a arquitetura do container, independentemente de o host ser Windows ou Mac.
5. **Execução:** Configuração do comando de entrada para iniciar o servidor `uvicorn` na porta 8000.

### Impacto na SCM
A adoção do Docker trouxe benefícios tangíveis para o controle de configuração:

* **Portabilidade Total:** A aplicação, incluindo sua interface gráfica e motor de cálculo nativo, roda de forma idêntica em qualquer máquina.
* **Abstração de Complexidade:** Novos desenvolvedores não precisam configurar compiladores ou variáveis de ambiente no sistema operacional; o `docker build` resolve todas as dependências.
* **Imutabilidade:** A imagem gerada serve como um artefato imutável, garantindo que a versão testada no CI seja exatamente a mesma entregue na Release.


---

## 7. Versionamento e Releases

Para garantir a organização do ciclo de vida do software e comunicar claramente as mudanças, o projeto adotou o padrão Semantic Versioning (SemVer) (MAJOR.MINOR.PATCH).

As entregas foram estruturadas em dois marcos principais (milestones):

🏷️ v0.1.0 — Release Inicial (MVP)
Esta versão estabeleceu a baseline do projeto, focando na infraestrutura de backend e na validação do fluxo de CI/CD.

* Escopo:
   * Implementação dos endpoints principais (API Rest);
   * Integração e consumo de dados da API externa (Open Charge Map);
   * Containerização completa da aplicação (Dockerfile);
   * Configuração inicial do Pipeline de CI e testes automatizados básicos;
   * Habilitação da documentação via Swagger.
🏷️ v1.0.0 — Release Estável (Gold)
Marco de finalização do projeto, elevando o nível de maturidade da aplicação com a introdução de interface visual, otimização de performance e robustez no tratamento de erros.

* Novas Funcionalidades:
   * Interface Gráfica (GUI): Implementação de camada visual para facilitar a interação do usuário.
   * Visualização de Mapas: Geração dinâmica de mapas HTML das estações filtradas.
   * Simulação Assíncrona: Atualização de status em background (via asyncio) sem bloquear as requisições da API.
* Melhorias de Arquitetura e QA:
   * Motor de Cálculo Híbrido: Algoritmo resiliente que utiliza C para performance, com fallback automático para Python (garantindo compatibilidade entre Windows e Linux no CI).
   * QA Avançado: Ampliação da cobertura de testes, incluindo uso de Mocks para simulação de banco de dados e validação de casos de borda.
   * Controle e Rastreabilidade
A gestão das versões foi realizada através de Tags anotadas no Git, vinculadas a Releases no GitHub. Cada lançamento foi acompanhado pela atualização do arquivo CHANGELOG.md (seguindo o padrão Keep a Changelog), garantindo total rastreabilidade entre o código entregue e as funcionalidades documentadas.

---

##  8. Documentação


---

## 9. Lições aprendidas

---

## 10. Reflexões individuais

### Eryca
Por não vir da área de desenvolvimento, este projeto foi meu primeiro contato real com o ciclo completo de software e com as práticas de SCM. Então, antes de implementar qualquer funcionalidade, precisei aprender a configurar meu ambiente, compreender o funcionamento do repositório e me adaptar ao fluxo de trabalho colaborativo, fundamental para acompanhar o restante do processo.

Inicialmente, fiquei responsável por organizar e criar as issues, definindo critérios de aceitação claros, padronizando labels e planejando o fluxo de entrega. A partir disso, foi possível estruturar o trabalho no GitHub Projects usando o modelo kanban, com prioridades bem definidas. Também contribuí configurando elementos essenciais do repositório, como a estratégia de branching e a convenção de commits, garantindo padronização e melhor rastreabilidade do desenvolvimento. Cada uma dessas tarefas me ajudou a compreender na prática como a boa gestão de processos influencia diretamente a eficiência e a qualidade do projeto.

Também acompanhei algumas atividades relacionadas ao CI/CD, dando apoio na validação das alterações do pipeline e aproveitando a oportunidade para entender melhor o funcionamento. Algumas configurações, como execução dos testes, validação automática do build e integrações do Docker passaram a fazer mais sentido conforme eu participava das revisões e dos ajustes. É válido destacar que, para mim, o papel de desenvolvedora foi o mais desafiador. No entanto, a estrutura organizada do código inicial, implementado pelos colegas, facilitou minha adaptação. Ainda assim, enfrentei dificuldades típicas do trabalho colaborativo quando precisei sincronizar a branch local após já ter feito commits, revertendo alterações, resolvendo conflitos e evitando sobrescrever código de outros membros. Essas situações reforçaram a importância de pulls frequentes e comunicação clara.

Outro ponto que contribuiu muito para o trabalho em conjunto foi a implementação do template de Pull Requests, que trouxe mais clareza, uniformidade e facilitou a rastreabilidade. As issues também tiveram um papel essencial, servindo não só para organizar implementação e configuração, mas para registrar microatividades administrativas e alinhar a equipe sobre o andamento do projeto. Para complementar essa organização, usamos ainda uma planilha externa como um kanban rascunho, onde detalhamos papéis, prazos, tags e dependências, o que deixou tudo mais claro e previsível para todos.

Por fim, trabalhar com Rian e Renato foi extremamente positivo. Eles foram proativos, responsáveis e sempre dispostos a ajudar, compartilhando ideias e esclarecendo dúvidas. Esse apoio tornou o processo mais leve e permitiu que eu aprendesse de forma prática e colaborativa.

### Renato


### Rian
Esta disciplina foi um divisor de águas na minha formação, proporcionando minha primeira experiência aprofundada em gerenciamento de projetos de software. Foi fundamental para que eu pudesse aprender na prática sobre Git, GitHub e todo o ciclo de vida de desenvolvimento.

Pela primeira vez, utilizei ferramentas de controle de versão de forma estruturada. Percebi o valor imenso de manter o código organizado, permitindo visualizar o histórico de alterações e, principalmente, a segurança de poder reverter a aplicação para um estado funcional caso algo desse errado. Outro ponto alto foi o aprendizado sobre desenvolvimento colaborativo e simultâneo.

No início do projeto, fiquei encarregado de desenvolver a base da API, integrando os dados do Open Charge Map. Essa etapa consolidou meu entendimento sobre o fluxo de trabalho no Git: para cada nova funcionalidade, criávamos uma branch específica, que depois era mergeada na branch de desenvolvimento (dev), e só após validação seguia para a branch principal (main). Esse processo garantiu a integridade da aplicação.

Também tive meu primeiro contato prático com testes de software. Atuar como tester e criar scripts de verificação automática mudou minha percepção sobre a confiabilidade do código. Da mesma forma, a documentação — algo que eu não tinha o costume de priorizar — mostrou-se essencial para tornar o projeto compreensível.

Como consideração final, a experiência deste projeto foi enriquecedora, permitindo-me desenvolver e aprimorar diversas competências, desde o desenvolvimento de software e uso de Git/GitHub até a aplicação de metodologias ágeis. Trabalhar com a Eryca e com o Renato foi extremamente gratificante; a contribuição deles foi essencial para manter a organização do projeto e criar um ambiente de trabalho colaborativo e amigável, fator que considero importante para o sucesso de qualquer trabalho em equipe.
