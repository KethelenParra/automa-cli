from pathlib import Path
import shutil
import typer
from rich import print
from rich.table import Table

app = typer.Typer(help="Organiza arquivos (ex: Downloads) por categorias.")

CATEGORIES = {
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".avi"},
    "Code": {".py", ".js", ".ts", ".java", ".cs", ".html", ".css", ".json"},
}


def category_for(ext: str) -> str:
    ext = ext.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def _unique_dest(path: Path) -> Path:
    """Retorna um destino único adicionando sufixo " (1)", " (2)", ... se necessário."""
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


@app.command()
def by_type(
    folder: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Procura recursivamente"),
    ignore: list[str] = typer.Option(None, "--ignore", "-i", help="Nomes de pastas a ignorar (repetir para múltiplos)"),
    dry_run: bool = typer.Option(True, "--dry-run/--apply"),
):
    """Organiza arquivos por tipo. Por padrão apenas simula (dry-run).

    - `--recursive` varre subpastas.
    - `--ignore` permite pular pastas pelo nome.
    - Em caso de conflito, adiciona sufixo " (1)", " (2)".
    """
    folder = folder.resolve()
    ignore_set = set(ignore or [])

    iterator = folder.rglob("*") if recursive else folder.iterdir()
    files = [p for p in iterator if p.is_file() and not (set(p.parts) & ignore_set)]

    moves: list[tuple[Path, Path]] = []
    for f in files:
        cat = category_for(f.suffix)
        dest_dir = folder / cat
        dest = dest_dir / f.name
        if dest == f:
            continue
        moves.append((f, dest))

    if not moves:
        print("[yellow]Nada para organizar.[/]")
        raise typer.Exit()

    table = Table(title="Preview - Organizar por tipo")
    table.add_column("Arquivo")
    table.add_column("Destino")
    total_size = 0
    for src, dest in moves:
        try:
            total_size += src.stat().st_size
        except Exception:
            pass
        table.add_row(src.name, str(dest.parent.name) + "/")

    print(table)
    print(f"\nTotal de arquivos: [bold]{len(moves)}[/] — Tamanho total: [bold]{total_size:,}[/] bytes")

    moved = 0
    moved_bytes = 0
    for src, dest in moves:
        final_dest = dest
        if dest.exists():
            final_dest = _unique_dest(dest)

        print(f"{src.name} -> {final_dest.relative_to(folder)}")
        if not dry_run:
            final_dest.parent.mkdir(parents=True, exist_ok=True)
            if final_dest.exists():
                print(f"[red]Pulando (já existe):[/] {final_dest.name}")
                continue
            try:
                shutil.move(str(src), str(final_dest))
                moved += 1
                try:
                    moved_bytes += final_dest.stat().st_size
                except Exception:
                    pass
            except Exception as exc:
                print(f"[red]Erro ao mover {src.name}:[/] {exc}")

    if dry_run:
        print("\n[cyan]Dry-run ativo. Use --apply para mover de verdade.[/]")
    else:
        print(f"\n[green]Organização concluída.[/] Arquivos movidos: {moved} — {moved_bytes:,} bytes")
