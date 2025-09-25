#!/bin/bash
# UV Project - Linux Shell Wrapper
# Save this as uv-project.sh in the same directory as uv-project.py
# Make executable: chmod +x uv-project.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Check if Python is available
if ! command -v python3 &>/dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python and try again"
    exit 1
fi

# Check if UV is available
if ! command -v uv &>/dev/null; then
    echo "Error: UV is not installed or not in PATH"
    echo "Please install UV and try again"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/uv-project.py"

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: uv-project.py not found in $SCRIPT_DIR"
    echo "Please make sure uv-project.py is in the same directory as this script"
    exit 1
fi

# Show help if no arguments
if [ $# -eq 0 ]; then
    echo "UV Project - Custom UV Project Creator"
    echo
    echo "Usage:"
    echo "  uv-project.sh create PROJECT_NAME [--template TEMPLATE] [--target-dir DIR] [--author-name NAME] [--author-email EMAIL]"
    echo "  uv-project.sh list"
    echo "  uv-project.sh show TEMPLATE_NAME"
    echo "  uv-project.sh template TEMPLATE_NAME TEMPLATE_FILE"
    echo "  uv-project.sh restore [TEMPLATE_NAME or all]"
    echo
    echo "Examples:"
    echo "  uv-project.sh create myproject"
    echo "  uv-project.sh create mywebapp --template web"
    echo "  uv-project.sh create mycli --template cli --author-name \"John Doe\" --author-email \"john@example.com\""
    echo "  uv-project.sh list"
    echo "  uv-project.sh show basic"
    echo "  uv-project.sh template mytemplate /path/to/template.toml"
    echo "  uv-project.sh restore"
    echo "  uv-project.sh restore mytemplate"
    echo
    exit 0
fi

COMMAND="$1"
shift

case "$COMMAND" in
    create)
        if [ -z "$1" ]; then
            echo "Error: Project name is required"
            echo "Usage: uv-project.sh create PROJECT_NAME [options]"
            exit 1
        fi

        PROJECT_NAME="$1"
        shift

        PYTHON_CMD=(python3 "$PYTHON_SCRIPT" create "$PROJECT_NAME")

        while [ $# -gt 0 ]; do
            case "$1" in
                --template|-t)
                    shift
                    [ -z "$1" ] && { echo "Error: --template requires a value"; exit 1; }
                    PYTHON_CMD+=("--template" "$1")
                    ;;
                --target-dir)
                    shift
                    [ -z "$1" ] && { echo "Error: --target-dir requires a value"; exit 1; }
                    PYTHON_CMD+=("--target-dir" "$1")
                    ;;
                --author-name)
                    shift
                    [ -z "$1" ] && { echo "Error: --author-name requires a value"; exit 1; }
                    PYTHON_CMD+=("--author-name" "$1")
                    ;;
                --author-email)
                    shift
                    [ -z "$1" ] && { echo "Error: --author-email requires a value"; exit 1; }
                    PYTHON_CMD+=("--author-email" "$1")
                    ;;
                --force_hooks)
                    PYTHON_CMD+=("--force_hooks")
                    ;;
                *)
                    echo "Error: Unknown option \"$1\""
                    exit 1
                    ;;
            esac
            shift
        done

        echo "Creating project \"$PROJECT_NAME\"..."
        "${PYTHON_CMD[@]}"
        ;;

    list)
        echo "Listing available templates..."
        python3 "$PYTHON_SCRIPT" list
        ;;

    show)
        if [ -z "$1" ]; then
            echo "Error: Template name is required"
            echo "Usage: uv-project.sh show TEMPLATE_NAME"
            exit 1
        fi
        echo "Showing template \"$1\"..."
        python3 "$PYTHON_SCRIPT" show "$1"
        ;;

    template)
        if [ -z "$1" ] || [ -z "$2" ]; then
            echo "Error: Template name and file path are required"
            echo "Usage: uv-project.sh template TEMPLATE_NAME TEMPLATE_FILE"
            exit 1
        fi
        if [ ! -f "$2" ]; then
            echo "Error: Template file \"$2\" not found"
            exit 1
        fi
        echo "Creating custom template \"$1\" from \"$2\"..."
        python3 "$PYTHON_SCRIPT" template "$1" "$2"
        ;;

    restore)
        if [ -z "$1" ]; then
            echo "Restoring all default templates..."
            python3 "$PYTHON_SCRIPT" restore
        else
            echo "Restoring template \"$1\" to default..."
            python3 "$PYTHON_SCRIPT" restore "$1"
        fi
        ;;

    *)
        echo "Error: Unknown command \"$COMMAND\""
        echo "Use \"uv-project.sh\" without arguments to see help"
        exit 1
        ;;
esac
