## CHANGELOG
Todas as mudanças importantes neste projeto serão documentadas neste arquivo.

O formato segue as recomendações do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e este projeto adota o versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [v1.0.1] - 2025-11-30
### Corrigido
- Ajuste nos nomes dos jobs do workflow nightly (`nightly_linux` e `nightly_windows`) para garantir compatibilidade e execução correta dos pipelines noturnos no GitHub Actions.

---

## [v1.0.0] - 2025-11-30
### Adicionado
- **Interface Gráfica (GUI):** Nova camada visual para facilitar o uso do simulador.
- **Visualização de Mapas:** Endpoint `/stations/city/{city_name}/map` que gera um mapa HTML das estações.
- **Motor Híbrido (C + Python):** Implementação de fallback automático. Se a biblioteca C (`.dll` ou `.so`) falhar, o Python assume o cálculo, garantindo compatibilidade entre Windows e Linux.
- **Simulação Assíncrona:** O ciclo de mudança de status das estações agora roda em background usando `asyncio`, sem bloquear a API.
- **Testes Mockados:** Novos testes unitários usando `unittest.mock` para validar a lógica de simulação sem depender de aleatoriedade.
- **Script de Execução:** Adicionado `run.bat` para facilitar a inicialização no Windows.

### Alterado
- Refatoração do `charging_engine.py` para suportar execução em ambientes sem bibliotecas compiladas (CI/CD).
- Atualização dos nomes das funções de cálculo no `main.py` para refletir a nova arquitetura do motor.

### Corrigido
- **CI/CD Linux:** Correção dos falhas no GitHub Actions causadas pela tentativa de carregar DLLs de Windows em ambiente Linux.
- **Linting:** Correção de erros de estilo (espaços em branco, imports não usados) apontados pelo Flake8.
- **Bugs de API:** Correção de erros 500 em casos de borda (bateria cheia ou inputs inválidos).

---

## [v0.1.0] - 2025-11-28
### Adicionado
- Conexão com API Open Charge Map
- Filtragem de pontos de recarga por cidade
- Cálculo de tempo de recarga
- Mudança de estado de estação (simulação)
- Endpoint `/health`
- Testes automatizados iniciais
- Workflow do GitHub Actions (build + tests)
- Workflow noturno com artefatos
- Dockerfile do projeto
- Seção "Como rodar via Docker" no README
- Template de Pull Request
- Melhorias de documentação
