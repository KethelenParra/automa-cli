import sys
from pathlib import Path

from typer.testing import CliRunner

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))

from automa_cli.cli import app


def test_backup_dry_run(tmp_path):
    src = tmp_path / "source"
    dst = tmp_path / "dest"
    src.mkdir()
    (src / "file1.txt").write_text("content1")
    (src / "file2.txt").write_text("content2")

    runner = CliRunner()
    result = runner.invoke(app, ["backup", "run", str(src), str(dst), "--dry-run"])
    assert result.exit_code == 0, result.output
    out = result.output
    assert "Dry-run ativo" in out
    assert "file1.txt" in out
    # destination should be empty (dry-run only)
    assert not (dst / "file1.txt").exists()


def test_backup_apply(tmp_path):
    src = tmp_path / "source"
    dst = tmp_path / "dest"
    src.mkdir()
    (src / "file1.txt").write_text("content1")
    (src / "subdir").mkdir()
    (src / "subdir" / "file2.txt").write_text("content2")

    runner = CliRunner()
    result = runner.invoke(app, ["backup", "run", str(src), str(dst), "--apply"])
    assert result.exit_code == 0, result.output
    out = result.output
    assert "Backup concluído" in out
    assert (dst / "file1.txt").exists()
    assert (dst / "subdir" / "file2.txt").exists()


def test_backup_exclude(tmp_path):
    src = tmp_path / "source"
    dst = tmp_path / "dest"
    src.mkdir()
    (src / "file1.txt").write_text("x")
    (src / "file2.log").write_text("x")
    (src / "file3.txt").write_text("x")

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["backup", "run", str(src), str(dst), "--exclude", "*.log", "--apply"]
    )
    assert result.exit_code == 0, result.output
    assert (dst / "file1.txt").exists()
    assert not (dst / "file2.log").exists()
    assert (dst / "file3.txt").exists()


def test_backup_incremental(tmp_path):
    src = tmp_path / "source"
    dst = tmp_path / "dest"
    src.mkdir()
    dst.mkdir()

    # first backup
    (src / "file1.txt").write_text("content1")
    runner = CliRunner()
    result = runner.invoke(app, ["backup", "run", str(src), str(dst), "--apply"])
    assert result.exit_code == 0
    assert (dst / "file1.txt").exists()

    # second backup: file1.txt unchanged, file2.txt new
    (src / "file2.txt").write_text("content2")
    result = runner.invoke(app, ["backup", "run", str(src), str(dst), "--apply"])
    assert result.exit_code == 0
    out = result.output
    # only file2.txt should be copied
    assert "file2.txt" in out
    assert (dst / "file2.txt").exists()
