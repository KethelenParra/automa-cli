from __future__ import annotations

import re
from pathlib import Path
import typer
from rich import print
from rich.table import Table

app = typer.Typer(help="Renomeia arquivos em massa com regras seguras.")

def slugify(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"[^a-z0-9._-]", "", name)
    return name

@app.command()
def slug(
    folder: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    recursive: bool = typer.Option(False, "--recursive", "-r"),
    dry_run: bool = typer.Option(True, "--dry-run/--apply", help="Por padrão só simula. Use --apply para renomear."),
):
    """
    Converte nomes para 'slug' (minúsculo, hífen, sem caracteres estranhos).
    """
    folder = folder.resolve()
    files = list(folder.rglob("*") if recursive else folder.glob("*"))
    files = [p for p in files if p.is_file()]
    table = Table(title="Preview - rename slug")
    table.add_column("Antes")
    table.add_column("Depois")

    changes: list[tuple[Path, Path]] = []
    for f in files:
        new_name = slugify(f.stem) + f.suffix.lower()
        if new_name != f.name:
            changes.append((f, f.with_name(new_name)))
            table.add_row(str(f.name), str(new_name))

    if not changes:
        print("[yellow]Nada para renomear.[/]")
        raise typer.Exit()

    print(table)
    print(f"\nTotal: [bold]{len(changes)}[/] mudanças")

    if dry_run:
        print("[cyan]Dry-run ativo: nada foi alterado. Use --apply para executar.[/]")
        raise typer.Exit()

    def _unique_path(path: Path) -> Path:
        if not path.exists():
            return path
        parent = path.parent
        stem = path.stem
        suffix = path.suffix
        i = 1
        while True:
            candidate = parent / f"{stem} ({i}){suffix}"
            if not candidate.exists():
                return candidate
            i += 1

    # aplicar com segurança
    renamed = 0
    for old, new in changes:
        final = new
        if new.exists():
            final = _unique_path(new)
            print(f"[yellow]Conflito, será usado:[/] {final.name}")
        try:
            final.parent.mkdir(parents=True, exist_ok=True)
            old.rename(final)
            renamed += 1
        except Exception as exc:
            print(f"[red]Erro renomeando {old.name} -> {final.name}:[/] {exc}")

    print(f"[green]Renomeação concluída.[/] Arquivos renomeados: {renamed}")
