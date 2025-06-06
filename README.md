# Task Note Manager

Task Note Manager to nowoczesna aplikacja webowa do zarządzania zadaniami i notatkami, napisana w Pythonie z wykorzystaniem frameworka Flask. Aplikacja oferuje intuicyjny interfejs użytkownika, zaawansowane funkcje organizacyjne i elastyczny system kategoryzacji.

## Funkcje

- **Zarządzanie zadaniami**
  - Tworzenie, edycja i usuwanie zadań
  - Ustawianie priorytetów (wysoki, średni, niski)
  - Przypisywanie terminów wykonania
  - Kategoryzacja zadań
  - Oznaczanie zadań jako wykonane

- **Zarządzanie notatkami**
  - Tworzenie, edycja i usuwanie notatek
  - Formatowanie tekstu
  - Kategoryzacja notatek
  - Szybki dostęp do najnowszych notatek

- **System kategorii**
  - Tworzenie własnych kategorii
  - Przypisywanie kolorów do kategorii
  - Filtrowanie zadań i notatek według kategorii

- **Statystyki i raporty**
  - Przegląd statystyk zadań według priorytetów
  - Statystyki notatek według kategorii
  - Wykresy i wizualizacje danych

## Wymagania techniczne

- Python 3.8+
- Flask 2.0+
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Bootstrap 5
- PostgreSQL

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/twoje-konto/task-note-manager.git
cd task-note-manager
```

2. Utwórz i aktywuj wirtualne środowisko:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Skonfiguruj zmienne środowiskowe:
```bash
cp .env.example .env
# Edytuj plik .env i ustaw odpowiednie wartości
```

5. Zainicjalizuj bazę danych:
```bash
flask db upgrade
```

6. Uruchom aplikację:
```bash
flask run
```

## Struktura projektu

```
task-note-manager/
├── app/
│   ├── auth/           # Moduł autoryzacji
│   ├── tasks/          # Moduł zadań
│   ├── notes/          # Moduł notatek
│   ├── categories/     # Moduł kategorii
│   ├── main/           # Moduł główny
│   ├── models/         # Modele danych
│   ├── templates/      # Szablony HTML
│   └── static/         # Pliki statyczne
├── migrations/         # Migracje bazy danych
├── tests/             # Testy jednostkowe
├── config.py          # Konfiguracja aplikacji
├── requirements.txt   # Zależności projektu
└── README.md          # Dokumentacja
```

## Testy

Aby uruchomić testy:
```bash
python -m pytest
```

## Licencja

Ten projekt jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku LICENSE.

## Autor

Grzegorz Żywicki

## Wersja

1.0.0
