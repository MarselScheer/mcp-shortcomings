# Repo Structure

A UV managed repo. Key paths/files:

- `Makefile` — Build and task automation commands
- `README.org` — Project documentation in Org mode format
- `src/main.py` — Main entry point for the application


# Development Commands

- `make run` — Run the application
- `make test` — Run all tests
- `make test-file TEST_FILE=path/to/test.py` — Run a single test file
- `make lint` — Lint code with ruff
- `make format` — Format code with ruff
- `make fix` — Auto-fix lint issues
- `make check` — Run all checks
