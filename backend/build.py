import os
import shutil
import subprocess
import sys
from pathlib import Path
from os import environ
from platform import system

# Get the root directory of the project
root = Path(__file__).parent

base = root.parent

if system() == "Linux":
    parent = "bin"
else:
    parent = "scripts"

ci_python = os.environ.get("pythonLocation")
virtual_env_path = environ.get("VIRTUAL_ENV", f"{base}/.venv")

SCRIPT_NAME = "backend"

if ci_python:
    python_path = Path(ci_python) / 'python'
    pyinstaller_path = Path(ci_python) / parent / 'pyinstaller'
else:
    python_path = Path(virtual_env_path) / parent / 'python'
    pyinstaller_path = Path(virtual_env_path) / parent / 'pyinstaller'

ci_requirements = root / "requirements-ci.txt"
requirements = root / "requirements.txt"

if __name__ == "__main__":
    print(f"{python_path}/{parent}/python")
    # Command to execute
    setup_command = [
        f"{python_path}",
        "-m",
        "pip",
        "install",
        "-r" f"{ci_requirements}",
    ]
    try:
        # Execute the command
        subprocess.check_call(setup_command, cwd=root)
    except subprocess.CalledProcessError as e:
        print("Error executing dev requirements install command:", e)
        sys.exit(1)
    req_command = [
        f"{python_path}",
        "-m",
        "pip",
        "install",
        "-r" f"{requirements}",
    ]
    try:
        # Execute the command
        subprocess.check_call(setup_command, cwd=root)
    except subprocess.CalledProcessError as e:
        print("Error executing requirements install command:", e)
        sys.exit(1)
    command = [
        f"{pyinstaller_path}",
        "main.py",
        "--noconsole",
        "--onefile",
        "--name",
        SCRIPT_NAME,
        "--collect-all",
        "uvicorn",
        "--noconfirm",
        "--clean",
        "--additional-hooks-dir",
        "extra-hooks",
    ]

    try:
        # Execute the command
        subprocess.check_call(command, cwd=root)
    except subprocess.CalledProcessError as e:
        print("Error executing pyinstaller command:", e)
        sys.exit(1)

    # Move the executable to the root directory
    # Create the destination folder if it doesn't exist
    destination_folder = base / "frontend" / "src" / "background"
    os.makedirs(destination_folder, exist_ok=True)
    pyinstaller_output_file = root / "dist" / f"{SCRIPT_NAME}.exe"
    # Copy the PyInstaller output file to the destination folder
    print("copying to final location")
    shutil.copy(pyinstaller_output_file, destination_folder)
    print("file copied")
