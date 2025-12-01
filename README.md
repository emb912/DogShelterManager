# DogShelterManager
System do zarządzania schroniskiem dla psów, który umożliwia monitorowanie wypełnienia schroniska w czasie rzeczywistym.
Umożliwia dodawanie, edycję, usuwanie psów, a po każdej zmianie wypełnienie schroniska jest aktualizowane za pomocą WebSocketa.

## Funkcjonalności aplikacji
- operacje CRUD na psach
- status serwera - wyświetlane data ostatniej aktualizacji i status połączenia z serwerem 
- monitorowanie poziomu wypełnienia schroniska - po każdej aktualizacji, automatycznie jest wysyłany zaktualizowany stan
- dokumentacja API wygenerowana automatycznie przez Swagger

## Technologie
Backend:
- FastAPI + SQLAlchemy
- baza danych: PostgreSQL
- WebSockets
- testy jednostkowe: pytest
Frontend:
- Next.js
- TypeScript
- Tailwind CSS
- React

## Struktura projektu
```
DogShelterManager/
├── backend/
│   ├── app/
│   │   ├── __init__.py                # Inicjalizacja modułu aplikacji
│   │   ├── config.py                  # Konfiguracja aplikacji i bazy danych
│   │   ├── database.py                # Połączenie i sesje z bazą danych
│   │   ├── main.py                    # Główny plik uruchamiający FastAPI
│   │   ├── websocket_manager.py       # Obsługa połączeń WebSocket
│   │   ├── crud/
│   │   │   ├── __init__.py            # Inicjalizacja modułu CRUD
│   │   │   └── dog.py                 # Operacje CRUD dla modelu psa
│   │   ├── models/
│   │   │   ├── __init__.py            # Inicjalizacja modułu modeli
│   │   │   └── dog.py                 # Definicja modelu ORM psa
│   │   ├── routers/
│   │   │   ├── __init__.py            # Inicjalizacja modułu routerów
│   │   │   ├── dog.py                 # Endpointy API dla psów
│   │   │   └── ws.py                  # Endpointy WebSocket
│   │   ├── schemas/
│   │   │   ├── __init__.py            # Inicjalizacja modułu schematów
│   │   │   └── dog.py                 # Schematy Pydantic dla psów
│   └── tests/
│       ├── database_test.py           # Konfiguracja połączenia testowego z bazą danych
│       ├── test_dogs.py               # Testy endpointów psów
│       └── test_ws.py                 # Testy WebSocket
├── frontend/
│   ├── index.html                     # Główny plik HTML aplikacji frontendowej
│   ├── package.json                   
│   └── src/
│       ├── App.css                    # Style głównej aplikacji
│       ├── App.tsx                    # Główny komponent React
│       ├── api/
│       │   └── dogs.ts                # Funkcje do komunikacji z API psów
│       ├── components/
│       │   ├── DogCard.tsx            # Komponent wyświetlający psa
│       │   ├── DogForm.tsx            # Formularz dodawania/edycji psa
│       │   └── StatsOverview.tsx      # Komponent statystyk schroniska
│       ├── hooks/
│       │   └── useSocket.ts           # Hook do obsługi WebSocket
│       ├── index.css                  
│       ├── main.tsx                   
│       └── types/
│           └── index.ts               # Typy TypeScript dla aplikacji
```

## Uruchomienie projektu
### 1. Klonowanie repozytorium
```
git clone https://github.com/emb912/DogShelterManager.git
cd DogShelterManager
```
### 2. Utworzenie bazy danych
- utwórz bazę danych dogsheltermanager w PostgreSQL
- wprowadź konieczne zmiany w pliku backend/.env
```
DATABASE_URL=postgresql+asyncpg://UZYTKOWNIK:HASLO@localhost:5432/dogsheltermanager
```
### 3. Utworzenie środowiska wirtualnego i instalacja zależności
```
cd backend
python -m venv .venv
.venv\Scripts\activate     # Windows
# lub
source .venv/bin/activate  # Linux / macOS
pip install -r requirements.txt
```
### 4. Instalacja zależności na frontendzie
```
cd frontend
npm install
```
### 5. Uruchomienie aplikacji
Backend: 
```
uvicorn app.main:app --reload
```
Frontend:
```
npm run dev
```
Dostęp do aplikacji:
Frontend: http://localhost:5173/
Backend API: http://localhost:8000/
Backend dokumentacja: http://localhost:8000/docs/

## Testy aplikacji
Zestaw testów jednostkowych dla backendu aplikacji Dog Shelter Manager. Testy pokrywają aspekty funkcjonalności API, takie jak: operacje CRUD, filtrowanie, sortowanie, działanie WebSockets oraz walidację danych.
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

### Utworzenie bazy danych do testów
- utwórz bazę danych dogsheltermanager_test w PostgreSQL
- wprowadź konieczne zmiany w pliku backend/.env
```
TEST_DATABASE_URL=postgresql://UZYTKOWNIK:HASLO@localhost:5432/dogsheltermanager_test
```
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