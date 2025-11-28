## ⚙️ Requisitos do Projeto

- **Python:** 3.11.2
- **Dependências:** Listadas em `requirements.txt`

Inclui:
- pytest, pytest-asyncio (testes automatizados)
- flake8 (linting)

Se necessário, atualize o arquivo `requirements.txt` para garantir que todas as bibliotecas utilizadas estejam listadas corretamente.

---

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

Isso garante que os imports funcionem corretamente durante os testes.
