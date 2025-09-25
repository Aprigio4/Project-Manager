# Publishing UV Project to PyPI

This guide explains how to publish the UV Project package to PyPI for easy installation via pip.

## Prerequisites

1. **PyPI Account**: Create accounts on both [PyPI](https://pypi.org) and [Test PyPI](https://test.pypi.org)
2. **API Tokens**: Generate API tokens for both PyPI and Test PyPI
3. **UV Installed**: Make sure UV is installed on your system

## Setup API Tokens

### For Test PyPI (recommended for testing):
1. Go to https://test.pypi.org/manage/account/token/
2. Generate a new API token
3. Export it as an environment variable:
```bash
export TEST_PYPI_API_TOKEN="your-test-token-here"
```

### For Production PyPI:
1. Go to https://pypi.org/manage/account/token/
2. Generate a new API token  
3. Export it as an environment variable:
```bash
export PYPI_API_TOKEN="your-production-token-here"
```

### Quick Setup for UV Publish:
You can also use UV's direct publish command:
```bash
# Set your token
export PYPI_API_TOKEN="pypi-your-token-here"

# Publish directly with UV
uv publish --token $PYPI_API_TOKEN
```

## Publishing Process

### Step 1: Test Publish (Recommended)

First, test your package on Test PyPI:

```bash
./publish.sh --test-publish
```

This will:
- Clean previous builds
- Build the package
- Upload to Test PyPI

### Alternative: Using UV Publish

UV also supports direct publishing:

```bash
# Set up authentication first (see Setup API Tokens section)
uv publish --token $PYPI_API_TOKEN
```

### Step 2: Test Installation

Test installing from Test PyPI:

```bash
pip install -i https://test.pypi.org/simple/ uv-project
```

### Step 3: Production Publish

Once you've verified everything works:

```bash
./publish.sh --publish
```

This will upload to the main PyPI.

### Step 4: Verify Installation

Test the production installation:

```bash
pip install uv-project
```

## Manual Publishing (Alternative)

If you prefer to publish manually:

```bash
# Build the package
uv build

# Install twine
uv tool install twine

# Upload to Test PyPI
twine upload --repository testpypi dist/* --username __token__ --password $TEST_PYPI_API_TOKEN

# Upload to PyPI
twine upload dist/* --username __token__ --password $PYPI_API_TOKEN
```

## Version Management

Before publishing:

1. Update the version in `pyproject.toml`:
```toml
[project]
name = "uv-project"
version = "0.2.0"  # Increment version
```

2. Update the changelog/release notes
3. Commit your changes
4. Tag the release:
```bash
git tag v0.2.0
git push origin v0.2.0
```

## Post-Publication

After successful publication:

1. **Update Documentation**: Ensure README.md reflects the latest features
2. **Create Release**: Create a GitHub release with changelog
3. **Test Installation**: Verify `pip install uv-project` works correctly
4. **Update Examples**: Ensure all examples in documentation work

## Package Structure

The published package includes:
- Python source code (`src/uv_create/`)
- Pre-commit configuration template
- Shell scripts for reference
- Documentation
- License file

## Users Can Install With:

```bash
# Standard installation
pip install uv-project

# Development installation
git clone https://github.com/Aprigio4/Project-Manager.git
cd Project-Manager
pip install -e .
```

## Usage After Installation:

```bash
# Create a new project
uv-project create my-project

# List templates
uv-project list

# Get help
uv-project --help
```

The package is now ready for smooth pip installation and distribution!