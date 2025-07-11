# Project manager

## Installation

### Windows

1. Install [UV](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

2. Clone the [Project-Manager](https://github.com/Aprigio4/Project-Manager)

3. Add Project Manager to Path so you can run it from anywhere:
   - Open the Start Menu and search for "Environment Variables"
   - Click on "Edit the system environment variables"
   - In the System Properties window, click on "Environment Variables"
   - Under "System variables", find the `Path` variable and click "Edit"
   - Click "New" and add the path to your cloned project manager directory (e.g., `C:\path\to\Project-Manager`)
   - Click OK to close all dialog boxes

### Linux

1. Install [UV](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

2. Clone the [Project-Manager](https://github.com/Aprigio4/Project-Manager)

3. Add Project Manager to Path so you can run it from anywhere:
   - Open a terminal and run:
   ```bash
   echo 'export PATH="$PATH:/path/to/Project-Manager"' >> ~/.bashrc
   source ~/.bashrc
   ```
## Usage
1. Open a terminal or command prompt
2. Navigate to the directory where you want to create a new project
3. Run the command:
```bash
   uv-project create <project-name>
```
4. Navigate into your new project directory:
```bash
   cd <project-name>
```
5. Sync your project with the following command:
```bash
   uv sync
```
6. Add new dependencies to your project:
```bash
   uv add <dependency-name>
```
7. Remove dependencies from your project:
```bash
   uv remove <dependency-name>
```
8. Check [Quality Assurance](docs\Quality-Assurance.md) to get more information about how to use the quality assurance features.
