#!/usr/bin/env python3
"""
Custom UV Create - A tool to create UV projects with custom .toml templates
"""

import argparse
import os
import shutil
import subprocess
from pathlib import Path


class UVCreateTemplate:
    def __init__(self, template_dir: str = None):
        self.template_dir = (
            Path(template_dir) if template_dir else Path.home() / ".uv_templates"
        )
        self.ensure_template_dir()

    def ensure_template_dir(self):
        """Ensure the template directory exists"""
        self.template_dir.mkdir(exist_ok=True)

        # Create default templates if they don't exist
        default_templates = {"basic": self.get_basic_template()}

        for template_name, template_content in default_templates.items():
            template_file = self.template_dir / f"{template_name}.toml"
            if not template_file.exists():
                with open(template_file, "w") as f:
                    f.write(template_content)

    def get_basic_template(self) -> str:
        """Basic project template"""
        return """

[project]
name = "{project_name}"
version = "0.1.0"
description = "A basic Python project"
authors = [
    {{name = "{author_name}", email = "{author_email}"}}
]
dependencies = []
readme = "README.md"
requires-python = ">=3.11"

[dependency-groups]
dev = [
    "pytest>=7.0",
    "black>=22.0",
    "ruff>=0.1.0",
    "pre-commit>=2.0.0",
    "mypy>=0.910"
]
[[tool.uv.index]]
name = "pytorch-cu118"
url = "https://download.pytorch.org/whl/cu118"
explicit = true

### CODE FORMATTING

[tool.black]
# https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length
line-length = 100
# Assume Python 3.11 (see `ruff`)
target-version = ['py311']
extend-exclude = '''
(
  ^/notebooks
  | ^/.pytest_cache
  | ^/.ruff_cache
)
'''

### CODE STYLE ENFORCEMENT

[tool.ruff]
fix = true
lint.select = [
    "A", "B", "C", "D", "E", "F", "G", "I", "N", "Q", "S", "T", "W", "ANN",
    "ARG", "BLE", "COM", "DJ", "DTZ", "EM", "ERA", "EXE", "FBT", "ICN", "INP",
    "ISC", "NPY", "PD", "PGH", "PIE", "PL", "PT", "PTH", "PYI", "RET", "RSE",
    "RUF", "SIM", "SLF", "TCH", "TID", "TRY", "UP", "YTT",
]
lint.ignore = ["D203", "D212", "D400", "D415", "PLR0913", "PLC0415"]
exclude = [
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
    "tests",
]
# Useful for pre-commit: https://beta.ruff.rs/docs/settings/#force-exclude
force-exclude = true
# https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length
line-length = 100
# Allow unused variables when underscore-prefixed.
# dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"
# Assume Python 3.11 (see `black`)
target-version = "py311"

[tool.ruff.lint.mccabe]
max-complexity = 10

### TYPE CHECKING

[tool.mypy]
files = "."
ignore_missing_imports = true
exclude = ["tests"]

### SECURITY

# NO CONFIGURATION REQUIRED. INCLUDED IN `ruff` (e.g., `bandit`) AND `pipenv check`.

### TESTING

[tool.pytest.ini_options]
addopts = "--cov --cov-fail-under=1 --dist=loadscope -n auto"

[tool.coverage.run]
source = ["."]

[tool.coverage.report]
show_missing = true
omit = ["*/tests/*"]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:"
]
"""

    def list_templates(self) -> list:
        """List available templates"""
        templates = []
        for template_file in self.template_dir.glob("*.toml"):
            templates.append(template_file.stem)
        return templates

    def create_project(
        self,
        project_name: str,
        template: str,
        target_dir: str = None,
        author_name: str = None,
        author_email: str = None,
    ):
        """Create a new project using the specified template"""

        # Set default values
        if not author_name:
            author_name = os.getenv("USER", "Your Name")
        if not author_email:
            author_email = f"{author_name.lower().replace(' ', '.')}@example.com"

        # Determine target directory
        if target_dir:
            project_path = Path(target_dir)
        else:
            project_path = Path.cwd() / project_name

        # Check if project already exists
        if project_path.exists():
            print(f"Error: Directory '{project_path}' already exists!")
            return False

        # Create project directory
        project_path.mkdir(parents=True)

        try:
            # Initialize with UV
            subprocess.run(
                ["uv", "init", str(project_path)], check=True, capture_output=True
            )

            # Load and process template
            template_file = self.template_dir / f"{template}.toml"
            if not template_file.exists():
                print(f"Error: Template '{template}' not found!")
                print(f"Available templates: {', '.join(self.list_templates())}")
                shutil.rmtree(project_path)
                return False

            with open(template_file, "r") as f:
                template_content = f.read()

            # Replace placeholders
            template_content = template_content.format(
                project_name=project_name,
                author_name=author_name,
                author_email=author_email,
            )

            # Write the customized pyproject.toml
            pyproject_path = project_path / "pyproject.toml"
            with open(pyproject_path, "w") as f:
                f.write(template_content)

            # Create additional files based on template type
            self.create_additional_files(project_path, template, project_name)

            print(
                f"✅ Successfully created project '{project_name}' using template '{template}'"
            )
            print(f"📁 Project location: {project_path}")
            print(f"🚀 Next steps:")
            print(f"   cd {project_name}")
            print(f"   uv sync")

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error running uv init: {e}")
            if project_path.exists():
                shutil.rmtree(project_path)
            return False
        except Exception as e:
            print(f"Error creating project: {e}")
            if project_path.exists():
                shutil.rmtree(project_path)
            return False

    def create_additional_files(
        self, project_path: Path, template: str, project_name: str
    ):
        """Create additional files based on the template type"""

        if template == "web":
            # Create main.py for web app
            main_file = project_path / "src" / project_name / "main.py"
            main_content = """from fastapi import FastAPI
        

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
"""
            with open(main_file, "w") as f:
                f.write(main_content)

        elif template == "cli":
            # Create cli.py for CLI app
            cli_file = project_path / "src" / project_name / "cli.py"
            cli_content = '''import click


@click.command()
@click.option('--name', default='World', help='Name to greet')
def main(name):
    """Simple CLI application"""
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    main()
'''
            with open(cli_file, "w") as f:
                f.write(cli_content)

        # copy .pre-commit-config to project
        pre_commit_config = Path(__file__).parent / ".pre-commit-config.yaml"
        if pre_commit_config.exists():
            shutil.copy(pre_commit_config, project_path / ".pre-commit-config.yaml")
            print("✅ Copied .pre-commit-config.yaml to project directory")
        else:
            print("Warning: .pre-commit-config.yaml not found, creating default config")
            pre_commit_content = """
repos:
  - repo: local
    hooks:

      ### CODE FORMATTING

      - id: black
        name: black
        stages: [ pre-commit ]
        language: system
        entry: pipenv run black .
        types: [ python ]

      ### CODE STYLE ENFORCEMENT

      - id: ruff
        name: ruff
        stages: [ pre-commit ]
        language: system
        entry: pipenv run ruff check .
        types: [ python ]

      ### TYPE CHECKING

      - id: mypy
        name: mypy
        stages: [ pre-commit ]
        language: system
        entry: pipenv run mypy .
        types: [ python ]
        pass_filenames: false

      ### SECURITY

      - id: check
        name: check
        stages: [ pre-push ]
        language: system
        entry: pipenv check
        types: [ python ]

      ### TESTING

      - id: pytest
        name: pytest
        stages: [ pre-push ]
        language: system
        entry: pipenv run pytest
        types: [ python ]
        pass_filenames: false

"""
            with open(project_path / ".pre-commit-config.yaml", "w") as f:
                f.write(pre_commit_content)
        print("✅ Created additional files based on template type")

    def create_custom_template(self, template_name: str, template_content: str):
        """Create a custom template"""
        template_file = self.template_dir / f"{template_name}.toml"
        with open(template_file, "w") as f:
            f.write(template_content)
        print(f"✅ Created custom template: {template_name}")

    def show_template(self, template_name: str):
        """Show the content of a template"""
        template_file = self.template_dir / f"{template_name}.toml"
        if not template_file.exists():
            print(f"Error: Template '{template_name}' not found!")
            return

        with open(template_file, "r") as f:
            content = f.read()

        print(f"Template: {template_name}")
        print("=" * 50)
        print(content)

    def reset_default_template(self, template_name: str = "all"):
        """Reset a template to its default content"""
        default_templates = {"basic": self.get_basic_template()}
        if template_name == "all":
            for name in default_templates:
                self.reset_default_template(name)
            print("✅ Reset all templates to default content")
            return

        if template_name not in default_templates:
            print(f"Error: Template '{template_name}' does not exist!")
            return

        template_file = self.template_dir / f"{template_name}.toml"
        with open(template_file, "w") as f:
            f.write(default_templates[template_name])
        print(f"✅ Reset template '{template_name}' to default content")


def main():
    parser = argparse.ArgumentParser(
        description="Create UV projects with custom templates"
    )
    parser.add_argument("--template-dir", help="Directory containing templates")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create project command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("project_name", help="Name of the project")
    create_parser.add_argument(
        "--template", "-t", default="basic", help="Template to use (default: basic)"
    )
    create_parser.add_argument("--target-dir", help="Target directory for the project")
    create_parser.add_argument("--author-name", help="Author name")
    create_parser.add_argument("--author-email", help="Author email")

    # List templates command
    list_parser = subparsers.add_parser("list", help="List available templates")

    # Show template command
    show_parser = subparsers.add_parser("show", help="Show template content")
    show_parser.add_argument("template_name", help="Name of the template to show")

    # Create template command
    template_parser = subparsers.add_parser("template", help="Create a custom template")
    template_parser.add_argument("template_name", help="Name of the template")
    template_parser.add_argument("template_file", help="Path to the template TOML file")

    # Restore backup command
    restore_parser = subparsers.add_parser(
        "restore", help="Restore templates from backup"
    )
    restore_parser.add_argument(
        "template_name",
        default="all",
        help="Name of the template to restore (default: all)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    creator = UVCreateTemplate(args.template_dir)

    if args.command == "create":
        creator.create_project(
            args.project_name,
            args.template,
            args.target_dir,
            args.author_name,
            args.author_email,
        )
    elif args.command == "list":
        templates = creator.list_templates()
        print("Available templates:")
        for template in templates:
            print(f"  - {template}")
    elif args.command == "show":
        creator.show_template(args.template_name)
    elif args.command == "template":
        with open(args.template_file, "r") as f:
            content = f.read()
        creator.create_custom_template(args.template_name, content)
    elif args.command == "restore":
        creator.reset_default_template(template_name=args.template_name)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help


if __name__ == "__main__":
    main()
