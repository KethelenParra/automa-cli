import sys
from pathlib import Path

from typer.testing import CliRunner

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))

from automa_cli.cli import app


def test_rename_slug_dry_run(tmp_path):
    d = tmp_path / "files"
    d.mkdir()
    (d / "My File.TXT").write_text("x")
    (d / "Another File.PDF").write_text("x")

    runner = CliRunner()
    result = runner.invoke(app, ["rename", "slug", str(d), "--dry-run"])
    assert result.exit_code == 0, result.output
    out = result.output
    assert "my-file.txt" in out.lower()
    assert "another-file.pdf" in out.lower()


def test_rename_slug_apply_handles_conflict(tmp_path):
    d = tmp_path / "files"
    d.mkdir()
    (d / "dup file.txt").write_text("a")
    (d / "dup-file.txt").write_text("b")

    runner = CliRunner()
    result = runner.invoke(app, ["rename", "slug", str(d), "--apply"])
    assert result.exit_code == 0, result.output

    files = list(d.glob("dup-file*"))
    assert len(files) >= 2
