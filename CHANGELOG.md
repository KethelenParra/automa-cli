# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-14

### Added
- **organize command**: Categorize files by type (Images, Documents, Archives, Audio, Video, Code)
  - `--recursive` flag for subdirectories
  - `--ignore` flag to exclude folder names
  - Safe duplicate handling with suffix numbering ` (1)`, ` (2)`, etc.
  - Preview table with file count and total size
  - `--dry-run` (default) and `--apply` modes

- **rename command**: Batch rename files to slug format (lowercase, hyphens, no special chars)
  - `--recursive` flag for subdirectories
  - Safe conflict handling with automatic suffixes
  - Preview table before applying
  - `--dry-run` (default) and `--apply` modes

- **expenses command**: Generate expense reports from CSV
  - Support for `data`, `descricao`, `categoria`, `valor` columns
  - `--month` flag to filter by YYYY-MM format
  - `--top N` flag to show top categories
  - `--output` flag to export report as CSV
  - `--show-counts` flag (default: true) to display transaction count
  - Rich formatted table output

- **backup command**: Incremental backup with filters
  - Recursive directory backup with structure preservation
  - `--exclude` flag for glob patterns (repeat for multiple)
  - `--incremental` (default) or `--full` mode
  - Size comparison for incremental backups
  - `--dry-run` (default) and `--apply` modes
  - Preview table with file sizes and total size

- **Infrastructure**:
  - 11 comprehensive tests (pytest)
  - Rich CLI output with tables and colors
  - Professional `pyproject.toml` with metadata
  - `.gitignore` for Python/IDE/OS files
  - GitHub Actions CI/CD workflow
  - MIT License
  - Comprehensive README with examples

### Testing
- All commands include `--dry-run` by default (safety first)
- 11 tests covering dry-run, apply, conflict handling, filtering, and incremental operations
- Test coverage includes edge cases (duplicates, exclusions, errors)

### Documentation
- Complete README with installation, usage examples, and troubleshooting
- Inline help for all commands (`--help`)
- Clear output messages and summaries

## [Unreleased]

### Planned
- Compress backup option (zip, tar.gz)
- Scheduling support (cron-like tasks)
- Configuration file support
- Plugins/extensions API
- Multi-language support
