# Testy jednostkowe aplikacji
Zestaw testów dlajednostkowych backendu aplikacji Dog Shelter Manager. Testy pokrywają aspekty funkcjonalności API, takie jak: operacje CRUD, filtrowanie, sortowanie, działanie WebSockets oraz walidację danych.

## Struktura testów

### 1. `test_dogs.py` - Testy podstawowych operacji CRUD
#### Testy tworzenia
- `test_create_dog` - podstawowe tworzenie psa
- `test_create_dog_minimal_data` - tworzenie z minimalnymi wymaganymi polami
- `test_create_dog_invalid_size` - walidacja nieprawidłowego rozmiaru
- `test_create_dog_invalid_status` - walidacja nieprawidłowego statusu

#### Testy pobierania
- `test_get_dogs_list` - pobieranie listy wszystkich psów
- `test_get_empty_dogs_list` - pobieranie listy psów, gdy baza danych jest pusta
- `test_get_single_dog` - pobieranie pojedynczego psa po ID
- `test_get_non_existent_dog` - próba pobrania nieistniejącego psa

#### Testy aktualizacji
- `test_update_dog` - podstawowa aktualizacja
- `test_update_dog_name` - aktualizacja tylko imienia
- `test_update_dog_status` - zmiana statusu psa
- `test_update_dog_multiple_fields` - aktualizacja wielu pól jednocześnie
- `test_update_non_existent_dog` - próba aktualizacji nieistniejącego psa
- `test_update_preserves_unmodified_fields` - sprawdzenie czy niezmienione pola są zachowane

#### Testy usuwania
- `test_delete_dog` - podstawowe usuwanie
- `test_delete_non_existent_dog` - próba usunięcia nieistniejącego psa
- `test_delete_dog_by_id` - usuwanie konkretnego psa

### 2. `test_ws.py` - Testy WebSocket
#### Podstawowe testy WebSocket
- `test_websocket_connection` - nawiązywanie połączenia
- `test_websocket_initial_stats_empty` - początkowe statystyki dla pustej bazy
- `test_websocket_stats_after_add` - aktualizacja po dodaniu psa
- `test_websocket_stats_multiple_dogs` - statystyki dla wielu psów

#### Testy aktualizacji przez WebSocket
- `test_websocket_stats_after_update` - aktualizacja po zmianie statusu
- `test_websocket_stats_after_delete` - aktualizacja po usunięciu
- `test_websocket_multiple_updates` - wielokrotne aktualizacje
- `test_multiple_websocket_connections` - wiele jednoczesnych połączeń

## Uruchamianie testów

### Wszystkie testy
```bash
pytest
```

### Konkretny plik testowy
```bash
pytest tests/test_dogs.py
pytest tests/test_ws.py
```

### Konkretny test
```bash
pytest tests/test_dogs.py::test_create_dog
pytest tests/test_ws.py::test_websocket_connection
```