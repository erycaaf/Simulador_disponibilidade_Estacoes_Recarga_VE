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
## 6. Docker e Ambiente Reprodutível


---

## 7. Versionamento e Releases

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