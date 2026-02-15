import typer
from rich import print

from automa_cli.command.rename import app as rename_app
from automa_cli.command.organize import app as organize_app
from automa_cli.command.expenses import app as expenses_app
from automa_cli.command.backup import app as backup_app

app = typer.Typer(help="Automa CLI - automações do dia a dia (renomear, organizar, gastos, backup).")

app.add_typer(rename_app, name="rename")
app.add_typer(organize_app, name="organize")
app.add_typer(expenses_app, name="expenses")
app.add_typer(backup_app, name="backup")

@app.command()
def version():
    print("[bold green]Automa CLI[/] v0.1.0")

if __name__ == "__main__":
    app()
