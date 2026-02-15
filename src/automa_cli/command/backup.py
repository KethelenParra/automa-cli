from pathlib import Path
import shutil
import typer
from rich import print
from rich.table import Table
import fnmatch

app = typer.Typer(help="Faz backup de pastas (cópia com preservação de estrutura).")


@app.command()
def run(
    source: Path = typer.Argument(..., exists=True, file_okay=False),
    destination: Path = typer.Argument(..., file_okay=False),
    exclude: list[str] = typer.Option(None, "--exclude", "-e", help="Padrões de exclusão (glob, repetir para múltiplos)"),
    incremental: bool = typer.Option(True, "--incremental/--full", help="Compare tamanho para incremental (padrão) ou copie tudo"),
    dry_run: bool = typer.Option(True, "--dry-run/--apply"),
):
    """Faz backup recursivo com suporte a filtros e modo incremental.

    Por padrão é incremental (compara tamanho) e apenas simula (--dry-run).
    Use --apply para copiar de verdade. Use --exclude para pular padrões.
    """
    source = source.resolve()
    destination = destination.resolve()

    exclude_set = set(exclude or [])

    def should_exclude(path: Path) -> bool:
        name = path.name
        return any(fnmatch.fnmatch(name, pat) for pat in exclude_set)

    files = [p for p in source.rglob("*") if p.is_file() and not should_exclude(p)]

    if not files:
        print("[yellow]Não há arquivos para backup.[/]")
        raise typer.Exit()

    copies: list[tuple[Path, Path]] = []
    total_size = 0

    for f in files:
        rel = f.relative_to(source)
        dest_file = destination / rel

        if incremental and dest_file.exists():
            try:
                if dest_file.stat().st_size == f.stat().st_size:
                    continue
            except Exception:
                pass

        copies.append((f, dest_file))
        try:
            total_size += f.stat().st_size
        except Exception:
            pass

    if not copies:
        print("[yellow]Nada para fazer (backup já atualizado ou tudo excluído).[/]")
        raise typer.Exit()

    table = Table(title="Preview - Backup")
    table.add_column("Arquivo (relativo)")
    table.add_column("Destino")
    table.add_column("Tamanho", justify="right")

    for src, dst in copies:
        rel = src.relative_to(source)
        try:
            size_str = f"{src.stat().st_size:,} B"
        except Exception:
            size_str = "?"
        table.add_row(str(rel), str(dst.relative_to(destination.parent)), size_str)

    print(table)
    print(f"\nArquivos a copiar: [bold]{len(copies)}[/] — Tamanho total: [bold]{total_size:,}[/] bytes")

    if dry_run:
        print("[cyan]Dry-run ativo. Use --apply para copiar de verdade.[/]")
        raise typer.Exit()

    copied = 0
    copied_bytes = 0
    for src, dst in copies:
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
            try:
                copied_bytes += dst.stat().st_size
            except Exception:
                pass
            print(f"✓ {src.relative_to(source)}")
        except Exception as exc:
            print(f"[red]✗ Erro ao copiar {src.relative_to(source)}:[/] {exc}")

    print(f"\n[green]Backup concluído.[/] Arquivos copiados: {copied} — {copied_bytes:,} bytes")
