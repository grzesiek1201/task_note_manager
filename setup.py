import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(command, shell=True):
    """Wykonuje komendę i wyświetla jej output"""
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
    """Konfiguruje środowisko i uruchamia aplikację"""
    print("=== Rozpoczynam konfigurację aplikacji ===")
    
    # 1. Sprawdź czy Python jest zainstalowany
    if sys.version_info < (3, 8):
        print("Wymagany jest Python 3.8 lub nowszy!")
        sys.exit(1)
    
    # 2. Utwórz wirtualne środowisko jeśli nie istnieje
    if not os.path.exists("venv"):
        print("\n=== Tworzenie wirtualnego środowiska ===")
        run_command("python -m venv venv")
    
    # 3. Aktywuj wirtualne środowisko i zainstaluj zależności
    print("\n=== Instalacja zależności ===")
    if os.name == 'nt':  # Windows
        run_command("venv\\Scripts\\pip install -r requirements.txt")
    else:  # Linux/Mac
        run_command("venv/bin/pip install -r requirements.txt")
    
    # 4. Skonfiguruj zmienne środowiskowe
    print("\n=== Konfiguracja zmiennych środowiskowych ===")
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("Utworzono plik .env z przykładowej konfiguracji")
        else:
            print("UWAGA: Brak pliku .env.example!")
    
    # 5. Inicjalizacja bazy danych
    print("\n=== Inicjalizacja bazy danych ===")
    if os.name == 'nt':  # Windows
        run_command("venv\\Scripts\\flask db init")
        run_command("venv\\Scripts\\flask db migrate")
        run_command("venv\\Scripts\\flask db upgrade")
    else:  # Linux/Mac
        run_command("venv/bin/flask db init")
        run_command("venv/bin/flask db migrate")
        run_command("venv/bin/flask db upgrade")
    
    print("\n=== Konfiguracja zakończona pomyślnie! ===")
    print("\nAby uruchomić aplikację:")
    if os.name == 'nt':  # Windows
        print("1. Aktywuj środowisko: .\\venv\\Scripts\\activate")
        print("2. Uruchom aplikację: flask run")
    else:  # Linux/Mac
        print("1. Aktywuj środowisko: source venv/bin/activate")
        print("2. Uruchom aplikację: flask run")

if __name__ == "__main__":
    setup_environment() 