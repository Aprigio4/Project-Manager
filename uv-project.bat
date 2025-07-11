@echo off
REM UV Create - Windows Batch Wrapper
REM Save this as uv-create.bat in the same directory as uv-create.py

setlocal enabledelayedexpansion

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    exit /b 1
)

REM Check if UV is available
uv --version >nul 2>&1
if errorlevel 1 (
    echo Error: UV is not installed or not in PATH
    echo Please install UV and try again
    exit /b 1
)

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%uv-create.py"

REM Check if the Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo Error: uv-create.py not found in %SCRIPT_DIR%
    echo Please make sure uv-create.py is in the same directory as this batch file
    exit /b 1
)

REM If no arguments provided, show help
if "%~1"=="" (
    echo UV Create - Custom UV Project Creator
    echo.
    echo Usage:
    echo   uv-create create PROJECT_NAME [--template TEMPLATE] [--target-dir DIR] [--author-name NAME] [--author-email EMAIL]
    echo   uv-create list
    echo   uv-create show TEMPLATE_NAME
    echo   uv-create template TEMPLATE_NAME TEMPLATE_FILE
    echo   uv-create update TEMPLATE_NAME TEMPLATE_FILE
    echo   uv-create update-all TEMPLATES_DIR
    echo.
    echo Examples:
    echo   uv-create create myproject
    echo   uv-create create mywebapp --template web
    echo   uv-create create mycli --template cli --author-name "John Doe" --author-email "john@example.com"
    echo   uv-create list
    echo   uv-create show basic
    echo   uv-create template mytemplate path\to\template.toml
    echo   uv-create restore [mytemplate or all]
    echo.
    echo Available commands:
    echo   create     - Create a new project using a template
    echo   list       - List available templates
    echo   show       - Show template content
    echo   template   - Create a custom template
    echo   restore    - Restore a template to its default
    echo.
    goto :end
)

REM Parse the command
set "COMMAND=%~1"
shift

if /i "%COMMAND%"=="create" (
    goto :create
) else if /i "%COMMAND%"=="list" (
    goto :list
) else if /i "%COMMAND%"=="show" (
    goto :show
) else if /i "%COMMAND%"=="template" (
    goto :template
) else if /i "%COMMAND%"=="restore" (
    goto :restore
) else (
    echo Error: Unknown command "%COMMAND%"
    echo Use "uv-create" without arguments to see help
    exit /b 1
)

:create
REM Handle create command
if "%~1"=="" (
    echo Error: Project name is required
    echo Usage: uv-create create PROJECT_NAME [options]
    exit /b 1
)

set "PROJECT_NAME=%~1"
shift

REM Build the Python command
set "PYTHON_CMD=python "%PYTHON_SCRIPT%" create "%PROJECT_NAME%""

REM Parse remaining arguments
:parse_create_args
if "%~1"=="" goto :execute_create
if /i "%~1"=="--template" (
    if "%~2"=="" (
        echo Error: --template requires a value
        exit /b 1
    )
    set "PYTHON_CMD=!PYTHON_CMD! --template "%~2""
    shift
    shift
    goto :parse_create_args
) else if /i "%~1"=="-t" (
    if "%~2"=="" (
        echo Error: -t requires a value
        exit /b 1
    )
    set "PYTHON_CMD=!PYTHON_CMD! --template "%~2""
    shift
    shift
    goto :parse_create_args
) else if /i "%~1"=="--target-dir" (
    if "%~2"=="" (
        echo Error: --target-dir requires a value
        exit /b 1
    )
    set "PYTHON_CMD=!PYTHON_CMD! --target-dir "%~2""
    shift
    shift
    goto :parse_create_args
) else if /i "%~1"=="--author-name" (
    if "%~2"=="" (
        echo Error: --author-name requires a value
        exit /b 1
    )
    set "PYTHON_CMD=!PYTHON_CMD! --author-name "%~2""
    shift
    shift
    goto :parse_create_args
) else if /i "%~1"=="--author-email" (
    if "%~2"=="" (
        echo Error: --author-email requires a value
        exit /b 1
    )
    set "PYTHON_CMD=!PYTHON_CMD! --author-email "%~2""
    shift
    shift
    goto :parse_create_args
) else (
    echo Error: Unknown option "%~1"
    exit /b 1
)

:execute_create
echo Creating project "%PROJECT_NAME%"...
%PYTHON_CMD%
goto :end

:list
REM Handle list command
echo Listing available templates...
python "%PYTHON_SCRIPT%" list
goto :end

:show
REM Handle show command
if "%~1"=="" (
    echo Error: Template name is required
    echo Usage: uv-create show TEMPLATE_NAME
    exit /b 1
)
set "TEMPLATE_NAME=%~1"
echo Showing template "%TEMPLATE_NAME%"...
python "%PYTHON_SCRIPT%" show "%TEMPLATE_NAME%"
goto :end

:template
REM Handle template command
if "%~1"=="" (
    echo Error: Template name is required
    echo Usage: uv-create template TEMPLATE_NAME TEMPLATE_FILE
    exit /b 1
)
if "%~2"=="" (
    echo Error: Template file is required
    echo Usage: uv-create template TEMPLATE_NAME TEMPLATE_FILE
    exit /b 1
)
set "TEMPLATE_NAME=%~1"
set "TEMPLATE_FILE=%~2"

REM Check if template file exists
if not exist "%TEMPLATE_FILE%" (
    echo Error: Template file "%TEMPLATE_FILE%" not found
    exit /b 1
)

echo Creating custom template "%TEMPLATE_NAME%" from "%TEMPLATE_FILE%"...
python "%PYTHON_SCRIPT%" template "%TEMPLATE_NAME%" "%TEMPLATE_FILE%"
goto :end

:restore
REM Handle update command
if "%~1"=="" (
    echo Restoring all default templates...
    python "%PYTHON_SCRIPT%" restore
    goto :end
)

set "TEMPLATE_NAME=%~1"
echo Restoring template "%TEMPLATE_NAME%" to default...
python "%PYTHON_SCRIPT%" restore "%TEMPLATE_NAME%"
goto :end

:end
endlocal