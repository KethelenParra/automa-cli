# 🛠️ Automa CLI — Automações do dia a dia

Uma CLI leve e poderosa para automações cotidianas: **organizar downloads, renomear arquivos em massa, gerar relatórios de gastos e fazer backup**.

**Status**: 4 comandos implementados | 11 testes passando | Pronto para PyPI

---

## ✨ Features

- ✅ **Organize**: Categorize arquivos por tipo (Imagens, Documentos, ZIP, Áudio, Vídeo, Código)
- ✅ **Rename**: Converta nomes para slug (minúsculo, hífen, sem caracteres estranhos)
- ✅ **Expenses**: Gere relatórios de gastos (CSV → tabela → export)
- ✅ **Backup**: Faça backup recursivo com filtros e modo incremental
- ✅ Todas com `--dry-run` por padrão (segurança primeiro)
- ✅ Preview em tabelas bonitas (Rich)
- ✅ Suporte a `--recursive`, `--exclude`, `--apply`
- ✅ Resumos com contagem e tamanho total

---

## 📦 Instalação

### Pré-requisitos

- Python 3.10+
- pip

### Opção 1: Instalar do repositório (desenvolvimento)

```bash
git clone https://github.com/KethelenParra/automa-cli.git
cd automa-cli
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -e .
```

Depois use de qualquer diretório:

```bash
automa --help
```

### Opção 2: Instalar via pip (quando publicado no PyPI)

```bash
pip install automa-cli
automa --help
```

---

## 🚀 Uso Rápido

### 1️⃣ Organizar Downloads

Categorize arquivos por tipo (Imagens, Documentos, Archives, etc).

```bash
# Preview (recomendado primeiro)
automa organize by-type "C:\Users\kethe\Downloads" --dry-run

# Aplicar de verdade
automa organize by-type "C:\Users\kethe\Downloads" --apply

# Recursivo (entra em subpastas)
automa organize by-type "C:\Users\kethe\Downloads" --recursive --apply

# Ignorar certas pastas
automa organize by-type "C:\Users\kethe\Downloads" --ignore ".git" --ignore "node_modules" --apply
```

**Output esperado:**

```
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Arquivo        ┃ Destino    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ photo.png      │ Images/    │
│ report.pdf     │ Documents/ │
│ archive.zip    │ Archives/  │
└────────────────┴────────────┘

Total de arquivos: 3 — Tamanho total: 5,234,567 bytes
Dry-run ativo. Use --apply para mover de verdade.
```

---

### 2️⃣ Renomear em Massa

Converta nomes para slug (minúsculo, hífen, sem caracteres especiais).

```bash
# Preview
automa rename slug "C:\Meus Documentos" --dry-run

# Aplicar
automa rename slug "C:\Meus Documentos" --apply

# Recursivo
automa rename slug "C:\Meus Documentos" --recursive --apply
```

**Exemplos de transformação:**

- `My File.TXT` → `my-file.txt`
- `Relatório 2026!.pdf` → `relatório-2026.pdf`
- `Ação & Resultado.docx` → `ação-resultado.docx`

---

### 3️⃣ Relatório de Gastos

Analise gastos a partir de CSV (data, descrição, categoria, valor).

**Formato esperado do CSV:**

```csv
data,descricao,categoria,valor
2026-02-01,Uber,Transporte,23.90
2026-02-02,Café,Alimentação,10.00
2026-02-03,Ônibus,Transporte,5.50
2026-02-10,Pizzaria,Alimentação,45.00
```

**Comandos:**

```bash
# Relatório completo (terminal)
automa expenses report gastos.csv

# Filtrar por mês
automa expenses report gastos.csv --month 2026-02

# Mostrar apenas top 3 categorias
automa expenses report gastos.csv --top 3

# Exportar relatório para CSV
automa expenses report gastos.csv --output relatorio.csv

# Sem mostrar quantidade de lançamentos
automa expenses report gastos.csv --show-counts=false
```

**Output esperado:**

```
Total: R$ 84.40

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Categoria      ┃ Valor       ┃ Lançamentos  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Alimentação    │ R$ 55.00    │ 2            │
│ Transporte     │ R$ 29.40    │ 2            │
└────────────────┴─────────────┴──────────────┘
```

---

### 4️⃣ Backup Automático

Faça backup recursivo com filtros e modo incremental.

```bash
# Preview
automa backup run "./Documentos" "./Backups" --dry-run

# Aplicar
automa backup run "./Documentos" "./Backups" --apply

# Excluir tipos de arquivo
automa backup run "./Docs" "./Backups" --exclude "*.tmp" --exclude "*.cache" --apply

# Modo full (copia tudo, não incremental)
automa backup run "./Docs" "./Backups" --full --apply

# Incremental (padrão: compara tamanho)
automa backup run "./Docs" "./Backups" --incremental --apply
```

**Output esperado:**

```
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Arquivo    ┃ Destino      ┃ Tamanho  ┃
┡━━━━━━━━━━━┇━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ file1.txt  │ Backups/file │ 1,024 B  │
│ file2.pdf  │ Backups/file │ 512 KB   │
└────────────┴──────────────┴──────────┘

Arquivos a copiar: 2 — Tamanho total: 525,312 bytes
Dry-run ativo. Use --apply para copiar de verdade.
```

---

## 🔧 Opções Globais

Todos os comandos suportam:

| Flag                | Descrição                               |
| ------------------- | --------------------------------------- |
| `--dry-run`         | (padrão) Simula sem alterar nada        |
| `--apply`           | Executa de verdade                      |
| `--help`            | Mostra ajuda do comando                 |
| `-r`, `--recursive` | Procura em subpastas (organize, rename) |
| `-e`, `--exclude`   | Exclui padrões (repetir para múltiplos) |

---

## 📋 Comandos Disponíveis

```bash
automa --help                          # Mostra todos os subcomandos
automa version                         # Mostra versão
automa organize --help                 # Ajuda do organize
automa rename --help                   # Ajuda do rename
automa expenses --help                 # Ajuda do expenses
automa backup --help                   # Ajuda do backup
```

---

## 🧪 Testes

Execute a suíte de testes (11 testes, todos passando):

```bash
python -m pytest -v

# Rodando no .venv:
.venv\Scripts\python.exe -m pytest -v
```

**Output esperado:**

```
tests/test_organize.py::test_organize_by_type_dry_run PASSED
tests/test_organize.py::test_organize_recursive_and_ignore PASSED
tests/test_organize.py::test_organize_apply_handles_duplicates PASSED
tests/test_rename.py::test_rename_slug_dry_run PASSED
tests/test_rename.py::test_rename_slug_apply_handles_conflict PASSED
tests/test_expenses.py::test_expenses_report_basic PASSED
tests/test_expenses.py::test_expenses_export_csv PASSED
tests/test_backup.py::test_backup_dry_run PASSED
tests/test_backup.py::test_backup_apply PASSED
tests/test_backup.py::test_backup_exclude PASSED
tests/test_backup.py::test_backup_incremental PASSED

===== 11 passed in 0.92s =====
```

---

## 📁 Estrutura do Projeto

```
automa-cli/
├── src/
│   └── automa_cli/
│       ├── __init__.py
│       ├── cli.py              # Ponto de entrada principal
│       └── command/
│           ├── organize.py     # Categorizar por tipo
│           ├── rename.py       # Slug + renomear
│           ├── expenses.py     # Relatório CSV
│           └── backup.py       # Backup com filtros
├── tests/
│   ├── test_organize.py
│   ├── test_rename.py
│   ├── test_expenses.py
│   └── test_backup.py
├── pyproject.toml              # Configuração e dependências
├── README.md                   # Este arquivo
└── .gitignore                  # Arquivos para ignorar no Git
```

---

## 🚀 Publicar no PyPI (pós-release)

Quando quiser publicar no PyPI:

```bash
# 1) Instalar ferramentas de build
pip install build twine

# 2) Gerar distribuição
python -m build

# 3) Upload (depois de criar conta em pypi.org)
python -m twine upload dist/*
```

Depois qualquer um instala com:

```bash
pip install automa-cli
```

---

## 💡 Exemplos de Uso Real

### Organizar Downloads após o mês

```bash
automa organize by-type "C:\Users\kethe\Downloads" --dry-run
# Revisar o preview
automa organize by-type "C:\Users\kethe\Downloads" --apply
```

### Renomear arquivos de um projeto antigo

```bash
automa rename slug "C:\Projetos\VelhoProjeto" --recursive --dry-run
automa rename slug "C:\Projetos\VelhoProjeto" --recursive --apply
```

### Gerar relatório mensal de gastos

```bash
automa expenses report gastos.csv --month 2026-02 --top 5 --output relatorio_fev.csv
```

### Fazer backup seguro (incremental)

```bash
automa backup run "C:\Meus Documentos" "D:\Backup" --exclude "*.tmp" --exclude ".git" --dry-run
automa backup run "C:\Meus Documentos" "D:\Backup" --exclude "*.tmp" --exclude ".git" --apply
```

---

## 📝 Dependências

- **typer** >= 0.12 — Framework para CLI
- **rich** >= 13.0 — Saída bonita (tabelas, cores)
- **pandas** >= 2.0 — Análise de dados (CSV)
- **python-dateutil** >= 2.8 — Parsing de datas

---

## 🐛 Problemas Comuns

### Erro: "automa: command not found"

- Certifique-se de ativar o venv: `source .venv/bin/activate` (Linux/Mac) ou `.venv\Scripts\activate` (Windows)
- Ou instale com `pip install -e .` na pasta do projeto.

### Erro: "No module named 'automa_cli'"

- Você está tentando rodar o script de um local diferente sem ativar o .venv?
- Use o caminho completo do Python:
  ```bash
  C:/Users/kethe/repository/automa-cli/.venv/Scripts/python.exe -m automa_cli.cli organize by-type "C:\Downloads" --dry-run
  ```

### Arquivo já existe no destino (organize/rename)

- O comando automaticamente adiciona sufixo ` (1)`, ` (2)`, etc.
- Não há conflitos — arquivos são renomeados com segurança.

### Backup incremental não funciona como esperado

- Use `--full` para copiar tudo, independente de tamanho
- Incremental (padrão) apenas copia se o tamanho for diferente

---

## 📄 Licença

MIT License — Sinta-se livre para usar, modificar e distribuir.

---

## 👨‍💻 Contribuições

Sugestões, correções e pull requests são bem-vindas!

```bash
git clone https://github.com/KethelenParra/automa-cli.git
cd automa-cli
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -e ".[dev]"
pytest
git checkout -b feature/sua-feature
# ... trabalhe ...
git push origin feature/sua-feature
```

---

## 📞 Suporte

Encontrou um problema? Abra uma [issue no GitHub]().

---

**Made with ❤️ para automações do dia a dia.**
