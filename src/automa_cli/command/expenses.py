from pathlib import Path
import typer
import pandas as pd
from rich import print
from rich.table import Table

app = typer.Typer(help="Gera relatórios de gastos a partir de CSV.")


@app.command()
def report(
    csv_file: Path = typer.Argument(..., exists=True, dir_okay=False),
    month: str = typer.Option(None, help="Filtrar por mês no formato YYYY-MM (ex: 2026-02)"),
    top: int = typer.Option(0, help="Mostrar apenas as N principais categorias (0 = todas)"),
    output: Path | None = typer.Option(None, help="Exportar relatório por categoria para CSV"),
    show_counts: bool = typer.Option(True, help="Mostrar quantidade de lançamentos por categoria"),
):
    df = pd.read_csv(csv_file)

    # normalizar colunas básicas
    required = {"data", "descricao", "categoria", "valor"}
    if not required.issubset(set(df.columns)):
        print(f"[red]CSV inválido. Precisa ter colunas: {sorted(required)}[/]")
        raise typer.Exit(code=1)

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["data", "valor"])

    if month:
        df = df[df["data"].dt.strftime("%Y-%m") == month]

    total = df["valor"].sum()

    agg = df.groupby("categoria")["valor"].agg(["sum", "count"]).rename(columns={"sum": "total", "count": "count"})
    agg = agg.sort_values("total", ascending=False)
    if top and top > 0:
        agg = agg.head(top)

    print(f"\n[bold]Total:[/] R$ {total:,.2f}")

    table = Table(title="Gastos por categoria")
    table.add_column("Categoria")
    table.add_column("Valor", justify="right")
    if show_counts:
        table.add_column("Lançamentos", justify="right")

    for cat, row in agg.iterrows():
        val = row["total"]
        if show_counts:
            table.add_row(str(cat), f"R$ {val:,.2f}", str(int(row["count"])) )
        else:
            table.add_row(str(cat), f"R$ {val:,.2f}")

    print(table)

    if output:
        out_df = agg.reset_index().rename(columns={"total": "valor"})
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            out_df.to_csv(output, index=False)
            print(f"[green]Relatório exportado para:[/] {output}")
        except Exception as exc:
            print(f"[red]Erro ao salvar CSV:[/] {exc}")
