# UV Project

A powerful command-line tool to create UV projects with custom templates, pre-configured development tools, and automated setup.

## Features

- 🚀 **Quick Project Creation**: Create new UV projects with a single command
- 📝 **Custom Templates**: Use built-in templates or create your own
- 🔧 **Pre-configured Tools**: Automatic setup of Black, Ruff, MyPy, and pytest
- 🪝 **Git Hooks**: Auto-install pre-commit and pre-push hooks
- ⚡ **UV Integration**: Full integration with UV package manager
- 🎯 **Multiple Templates**: Support for basic, web, CLI, and custom project types

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install uv-project
```

### Option 2: Install from Source

1. Install [UV](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

2. Clone this repository:
```bash
git clone https://github.com/Aprigio4/Project-Manager.git
cd Project-Manager
```

3. Install the package:
```bash
uv build
pip install dist/uv_project-*.whl
```

### Option 3: Development Installation

1. Clone the repository and install in development mode:
```bash
git clone https://github.com/Aprigio4/Project-Manager.git
cd Project-Manager
pip install -e .
```

## Usage

### Create a New Project

```bash
uv-project create my-project
```

### Create with Specific Template

```bash
uv-project create my-web-app --template web
```

### Create with Custom Author Info

```bash
uv-project create my-cli --template cli --author-name "John Doe" --author-email "john@example.com"
```

### List Available Templates

```bash
uv-project list
```

### View Template Details

```bash
uv-project show basic
```

### Create Custom Template

```bash
uv-project template my-template /path/to/template.toml
```

### Force Reinstall Pre-commit Hooks

```bash
uv-project create my-project --force_hooks
```

## Project Structure

After creating a project, you'll get:

```
my-project/
├── .git/                    # Git repository
├── .pre-commit-config.yaml  # Pre-commit configuration
├── .venv/                   # Virtual environment (after uv sync)
├── pyproject.toml           # Project configuration
├── README.md                # Project documentation
└── src/
    └── my_project/
        ├── __init__.py
        └── py.typed
```

## Available Templates

- **basic**: Standard Python project with development tools
- **web**: FastAPI web application template
- **cli**: Click-based CLI application template
- **custom**: Your own custom templates

## Development Tools Included

- **Black**: Code formatter
- **Ruff**: Fast Python linter
- **MyPy**: Static type checker
- **pytest**: Testing framework
- **pre-commit**: Git hooks for code quality

## Quick Start

1. Install UV Project:
   ```bash
   pip install uv-project
   ```

2. Create a new project:
   ```bash
   uv-project create awesome-project
   ```

3. Navigate and setup:
   ```bash
   cd awesome-project
   uv sync  # Install dependencies
   ```

4. Start coding:
   ```bash
   # Your project is ready with:
   # - Virtual environment
   # - Pre-commit hooks
   # - Development tools configured
   # - Git repository initialized
   ```
7. Remove dependencies from your project:
```bash
   uv remove <dependency-name>
```
8. Check [Quality Assurance](docs/Quality-Assurance.md) to get more information about how to use the quality assurance features.
