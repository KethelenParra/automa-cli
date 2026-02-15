# Contributing to Automa CLI

Obrigado por querer contribuir! Aqui estão as diretrizes.

## 🚀 Como Contribuir

### 1. Fork o repositório

```bash
git clone https://github.com/KethelenParra/automa-cli.git
cd automa-cli
```

### 2. Create uma branch feature

```bash
git checkout -b feature/sua-feature
# ou para bugfixes:
git checkout -b fix/bug-descricao
```

### 3. Configure o ambiente de desenvolvimento

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

pip install -e ".[dev]"
```

### 4. Implemente sua feature/correção

- Escreva código limpo e bem documentado
- Adicione testes para sua feature
- Certifique-se de que os testes passam:
  ```bash
  pytest -v
  ```

### 5. Commit e Push

```bash
git add .
git commit -m "feat: descrição clara da mudança"
git push origin feature/sua-feature
```

### 6. Abra um Pull Request

- Descreva o problema/feature claramente
- Referencie issues relacionadas (`Fixes #123`)
- Explique as mudanças feitas

## 🧪 Diretrizes para Testes

TODO: `src/automa_cli/command/seu_comando.py`

- Adicione função `test_seu_comando_*` em `tests/test_seu_comando.py`
- Cubra casos principais (dry-run, apply, errors)
- Use `tmp_path` fixture do pytest para arquivos temporários

Exemplo (teste básico):

```python
def test_novo_comando_dry_run(tmp_path):
    d = tmp_path / "test"
    d.mkdir()
    (d / "arquivo.txt").write_text("conteúdo")

    runner = CliRunner()
    result = runner.invoke(app, ["seu-comando", "acao", str(d), "--dry-run"])
    assert result.exit_code == 0
    assert "Dry-run ativo" in result.output
```

## 📋 Checklist antes de submeter PR

- [ ] Testes novos/atualizados passam localmente (`pytest -v`)
- [ ] Código segue padrão do projeto (sem `print()`, use `rich.print`)
- [ ] README/CHANGELOG atualizados (se apropriado)
- [ ] Commit message é descritivo
- [ ] Sem quebra de mudanças (ou documentado como breaking)

## 🐛 Reportar Bugs

Abra uma issue com:

- **Descrição clara** do problema
- **Passos para reproduzir**
- **Saída esperada vs atual**
- **Seu ambiente** (Python 3.10/3.11/3.12, SO, versão do CLI)

## 💡 Sugestões de Features

Abra uma discussion ou issue com tag `enhancement`:

- Descreva a feature e por que seria útil
- Exemplos de uso
- Impacto (compatibilidade com versões antigas)

## 📝 Estilo de Código

- Use type hints onde possível
- Docstrings em português ou inglês (consistente)
- 79-100 colunas por linha
- Use f-strings
- Importe de `rich` para saída formatada

## 🔗 Links Úteis

- [Typer Docs](https://typer.tiangolo.com/)
- [Rich Docs](https://rich.readthedocs.io/)
- [Pytest Docs](https://docs.pytest.org/)

---

**Obrigado por contribuir! 🎉**
