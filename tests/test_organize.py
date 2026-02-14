import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "src"
sys.path.insert(0, str(src))

from typer.testing import CliRunner

from automa_cli.cli import app


def test_organize_by_type_dry_run(tmp_path):
    d = tmp_path / "downloads"
    d.mkdir()
  
    (d / "img1.PNG").write_text("x")
    (d / "doc1.pdf").write_text("x")
    (d / "archive.zip").write_text("x")

    runner = CliRunner()
    result = runner.invoke(app, ["organize", "by-type", str(d), "--dry-run"])

    assert result.exit_code == 0, result.output
    out = result.output
    assert "Images/" in out or "Images" in out
    assert "Documents/" in out or "Documents" in out
    assert "Archives/" in out or "Archives" in out


def test_organize_recursive_and_ignore(tmp_path):
    d = tmp_path / "downloads"
    d.mkdir()
    sub = d / "sub"
    sub.mkdir()
    (sub / "img2.jpg").write_text("x")
    (d / "doc2.PDF").write_text("x")

    runner = CliRunner()
    result = runner.invoke(app, ["organize", "by-type", str(d), "--recursive", "--dry-run"])
    assert result.exit_code == 0, result.output
    out = result.output
    assert "Images/" in out
    assert "Documents/" in out


def test_organize_apply_handles_duplicates(tmp_path):
    d = tmp_path / "downloads"
    d.mkdir()
    images_dir = d / "Images"
    images_dir.mkdir()

    (images_dir / "dup.png").write_text("old")

    (d / "dup.png").write_text("new")

    runner = CliRunner()
    result = runner.invoke(app, ["organize", "by-type", str(d), "--apply"])
    assert result.exit_code == 0, result.output

    moved = list(images_dir.glob("dup*"))
    assert any(p.name == "dup.png" for p in moved)
    assert any(p.name != "dup.png" for p in moved)
