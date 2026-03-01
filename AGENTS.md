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
- `aspects/<aspect_name>/aspect.yaml` — information about a particular aspect
- `aspects/<aspect_name>/features/` — Each yaml file represents one features (status quo) of a particular aspect
- `aspects/<aspect_name>/shortcomings/` — Each yaml file represents one shortcoming of a particular aspect

# Core rules

- keep the AGENTS.md file updated, for instance if you create new development commands or modifies the repo structure
- adding a new aspect, feature, shortcoming should be done via the shortcoming-mcp
- updating/deleting an existing aspect, feature, shortcoming can be done directly in the corresponding yaml-file

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
- `make list-all-shortcomings` — expects parameter 'crit' and lists all shortcomings for all aspects
- `make list-shortcomings-of-aspect` — expects parameter 'crit' and 'aspect' list all shortcomings for one aspect
