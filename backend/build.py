import os
import shutil
import subprocess
import sys
from pathlib import Path

# Path to the Python virtual environment
root = Path(__file__).parent

base = root.parent

virtual_env_path = f"{base}/.venv"

SCRIPT_NAME = "backend"

if __name__ == "__main__":
    print(f"{virtual_env_path}/scripts/python")
    # Command to execute
    command = [
        f"{virtual_env_path}/scripts/pyinstaller",
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
