# Repo Structure

A UV managed repo. Key paths/files:

- `Makefile` — Build and task automation commands
- `README.org` — Project documentation in Org mode format
- `pyproject.toml` — Python project configuration
- `uv.lock` — UV lock file
- `src/main.py` — Main entry point for the application
- `src/models.py` — Data models
- `src/storage.py` — Storage layer
- `tests/test_storage.py` — Storage tests

# Core rules

- keep the AGENTS.md file updated, for instance if you create new development commands or modifies the repo structure

# Development Commands

- `make run` — Run the application
- `make test` — Run all tests
- `make test-file TEST_FILE=path/to/test.py` — Run a single test file
- `make lint` — Lint code with ruff
- `make format` — Format code with ruff
- `make fix` — Auto-fix lint issues
- `make check` — Run all checks
