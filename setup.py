import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(command, shell=True):
    """Execute a shell command and print its output.
    
    Args:
        command: The command to execute.
        shell: Whether to use shell execution (default: True).
        
    Returns:
        int: Return code of the executed command.
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=shell,
        universal_newlines=True
    )
    
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    return process.returncode

def setup_environment():
    """Set up the development environment for the application.
    
    This function:
    - Checks Python version requirements
    - Creates virtual environment if it doesn't exist
    - Installs required packages
    - Configures environment variables
    - Initializes the database
    
    Returns:
        None
    """
    print("=== Enviroment setup... ===")

    if sys.version_info < (3, 8):
        print("Required Python 3.8 or higher!")
        sys.exit(1)

    if not os.path.exists("venv"):
        print("\n=== Creating venv.... ===")
        run_command("python -m venv venv")

    print("\n=== Installing requirements===")
    if os.name == 'nt':  # Windows
        run_command("venv\\Scripts\\pip install -r requirements.txt")
    else:  # Linux/Mac
        run_command("venv/bin/pip install -r requirements.txt")

    print("\n=== Configuring environment ===")
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("Created file .env ")
        else:
            print("WARNING: No file .env.example!")
    

    print("\n=== Initializing data base ===")
    if os.name == 'nt':  # Windows
        run_command("venv\\Scripts\\flask db init")
        run_command("venv\\Scripts\\flask db migrate")
        run_command("venv\\Scripts\\flask db upgrade")
    else:  # Linux/Mac
        run_command("venv/bin/flask db init")
        run_command("venv/bin/flask db migrate")
        run_command("venv/bin/flask db upgrade")
    
    print("\n=== Configuration succesful! ===")
    print("\nTo run application:")
    if os.name == 'nt':  # Windows
        print("1. Active venv: .\\venv\\Scripts\\activate")
        print("2. Run application: flask run")
    else:  # Linux/Mac
        print("1. Active venv: source venv/bin/activate")
        print("2. Run application: flask run")

if __name__ == "__main__":
    setup_environment() 