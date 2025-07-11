# Quality Assurance
This module provides a set of tools for quality assurance in software development, including code analysis, testing, and reporting.

## Basic Usage
1. Check code formatting with Black
```bash
uv run black .
``` 
2. Check code quality with Ruff
```bash
uv run ruff check .
``` 
3. Type check with MyPy
```bash
uv run mypy .
```
4. Run tests with Pytest
```bash
uv run pytest .
```
5. Generate test coverage report
```bash
uv run pytest --cov --cov-report=html
```

## Pre-commit
To ensure code quality before committing, you can set up pre-commit hooks.
1. Install the pre-commit hooks 
```bash
uv run pre-commit install -t pre-commit
```
2. Install the pre-push hooks
```bash
uv run pre-commit install -t pre-push
```
3. Run pre-commit hooks manually
```bash
uv run pre-commit run --all-files --hook-stage commit
```
```bash
uv run pre-commit run --all-files --hook-stage push
```