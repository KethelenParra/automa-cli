import sys
from pathlib import Path

from typer.testing import CliRunner

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))

from automa_cli.cli import app


def _write_csv(path: Path, rows: list[tuple]):
    # rows: list of (data, descricao, categoria, valor)
    import csv

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["data", "descricao", "categoria", "valor"])
        for r in rows:
            w.writerow(r)


def test_expenses_report_basic(tmp_path):
    csv = tmp_path / "gastos.csv"
    rows = [
        ("2026-02-01", "Uber", "Transporte", "23.90"),
        ("2026-02-02", "Cafe", "Alimentacao", "10.00"),
        ("2026-02-03", "Onibus", "Transporte", "5.50"),
    ]
    _write_csv(csv, rows)

    runner = CliRunner()
    result = runner.invoke(app, ["expenses", "report", str(csv)])
    assert result.exit_code == 0, result.output
    out = result.output
    assert "Total:" in out
    assert "Transporte" in out
    assert "Alimentacao" in out


def test_expenses_export_csv(tmp_path):
    csv = tmp_path / "gastos.csv"
    out_csv = tmp_path / "out.csv"
    rows = [
        ("2026-02-01", "Uber", "Transporte", "23.90"),
        ("2026-02-02", "Cafe", "Alimentacao", "10.00"),
        ("2026-02-03", "Onibus", "Transporte", "5.50"),
    ]
    _write_csv(csv, rows)

    runner = CliRunner()
    result = runner.invoke(app, ["expenses", "report", str(csv), "--output", str(out_csv)])
    assert result.exit_code == 0, result.output
    assert out_csv.exists()
    content = out_csv.read_text(encoding="utf-8")
    assert "Transporte" in content
