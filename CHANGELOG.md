# Changelog


## [1.0.0] - 2025-06-06

### Dodano
- Podstawową strukturę aplikacji Flask
- System autoryzacji użytkowników
- Moduł zarządzania zadaniami
  - Tworzenie, edycja i usuwanie zadań
  - Ustawianie priorytetów
  - Przypisywanie terminów
  - Kategoryzacja
- Moduł zarządzania notatkami
  - Tworzenie, edycja i usuwanie notatek
  - Formatowanie tekstu
  - Kategoryzacja
- System kategorii
  - Tworzenie i zarządzanie kategoriami
  - Przypisywanie kolorów
- Panel główny z widokiem statystyk
  - Statystyki zadań według priorytetów
  - Statystyki notatek według kategorii
- Responsywny interfejs użytkownika
  - Bootstrap 5
  - Ikony Bootstrap Icons
  - Kolorowe oznaczenia priorytetów
- System migracji bazy danych
- Podstawowe testy jednostkowe

### Zmieniono
- Zoptymalizowano strukturę projektu
- Poprawiono wydajność zapytań do bazy danych
- Ulepszono interfejs użytkownika

### Naprawiono
- Problem z importami cyklicznymi
- Błędy w walidacji formularzy
- Problemy z wyświetlaniem statystyk 