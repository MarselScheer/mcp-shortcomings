# Repo Structure

A UV managed repo. Key paths/files:

- `Makefile` — Build and task automation commands
- `README.org` — Project documentation in Org mode format
- `pyproject.toml` — Python project configuration
- `uv.lock` — UV lock file
- `src/main.py` — Main entry point for the application
- `src/mcp_server.py` — MCP (Model Context Protocol) server implementation
- `src/models.py` — Data models
- `src/storage.py` — Storage layer
- `tests/test_storage.py` — Storage tests
- `tests/test_mcp_server.py` — MCP server tests
- `aspects/` — Aspects, features and shortcomings definitions

# Core rules

- keep the AGENTS.md file updated, for instance if you create new development commands or modifies the repo structure

# Development Commands

Do NOT use `cd` before make targets; make handles directory context internally (e.g., use `make test` not `cd . && make test`)

- `make run` — Run the application
- `make test` — Run all tests
- `make test-file TEST_FILE=path/to/test.py` — Run a single test file
- `make lint` — Lint code with ruff
- `make format` — Format code with ruff
- `make fix` — Auto-fix lint issues
- `make typecheck` — Type check with ty
- `make check` — Run all checks (lint + typecheck)
