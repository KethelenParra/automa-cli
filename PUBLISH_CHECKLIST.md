# 📋 Checklist para Publicação

Antes de fazer push no GitHub e publicar no PyPI, percorra este checklist:

## ✅ Repositório Local

- [x] 4 comandos implementados (organize, rename, expenses, backup)
- [x] 11 testes passando 
- [x] README.md completo com exemplos
- [x] .gitignore adequado (venv, __pycache__, etc)
- [x] pyproject.toml com metadados profissionais
- [x] CHANGELOG.md documentando versão 0.1.0
- [x] LICENSE (MIT)
- [x] CONTRIBUTING.md com guia
- [x] GitHub Actions workflow (tests.yml)

## 🔧 Antes de fazer commit/push

1. **Substitua seus dados no pyproject.toml:**
   ```toml
   authors = [
       {name = "Seu Nome", email = "seu-email@example.com"}
   ]
   
   [project.urls]
   Homepage = "https://github.com/SEU-USUARIO/automa-cli"
   Repository = "https://github.com/SEU-USUARIO/automa-cli.git"
   Issues = "https://github.com/SEU-USUARIO/automa-cli/issues"
   ```

2. **No README.md, substitua URLs:**
   - Mude `seu-usuario` para seu GitHub username
   - Mude URLs de exemplo em "Publicar no PyPI"

3. **No CONTRIBUTING.md, substitua:**
   - URLs do fork/repositório

4. **Rode testes uma última vez:**
   ```bash
   python -m pytest -v
   ```

## 📤 Publicar no GitHub

1. **Crie repositório no GitHub:**
   - Vá para https://github.com/new
   - Nome: `automa-cli`
   - Descrição: "Automações do dia a dia: organizar, renomear, relatório de gastos, backup"
   - Público (para portfólio)
   - Não inicializa com README (já tem um)

2. **Configure git local:**
   ```bash
   cd C:\Users\kethe\repository\automa-cli
   git remote remove origin  # se existir
   git remote add origin https://github.com/SEU-USUARIO/automa-cli.git
   git branch -M main
   git push -u origin main
   ```

3. **Verifique no GitHub:**
   - Vá para seu repositório
   - Confirme que README.md, testes, etc estão lá
   - Checks de workflow devem estar rodando (Actions)

## 🎉 Publicar no PyPI (opcional, depois)

1. **Criar conta no PyPI:**
   - https://pypi.org/account/register/
   - Ative 2FA

2. **Instalar ferramentas de build:**
   ```bash
   pip install build twine
   ```

3. **Gerar distribuição:**
   ```bash
   python -m build
   ```

4. **Upload para PyPI (test antes du prod):**
   ```bash
   # Test PyPI (recomendado primeiro):
   python -m twine upload --repository testpypi dist/*
   
   # Produção PyPI (depois de confirmar):
   python -m twine upload dist/*
   ```

5. **Testar instalação:**
   ```bash
   pip install automa-cli
   automa --help
   ```

## 🚀 Depois de publicar

- [ ] Atualizar links nos comentários de código
- [ ] Criar releases no GitHub (v0.1.0, v0.2.0, etc)
- [ ] Considerar adicionar badges ao README (build, PyPI downloads, licença)
- [ ] Documentar em seu portfólio/CV

## 📚 Referências

- [Typer CLI Tool](https://typer.tiangolo.com/)
- [Rich Text Formatting](https://rich.readthedocs.io/)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

---

**Status:** Pronto para publicar! ✨
