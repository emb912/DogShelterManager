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
- Vite
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
DATABASE_URL=postgresql://UZYTKOWNIK:HASLO@localhost:5432/dogsheltermanager
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
- Frontend: http://localhost:5173/
- Backend API: http://localhost:8000/
- Backend dokumentacja: http://localhost:8000/docs/

## Testy aplikacji
Zestaw testów jednostkowych dla backendu aplikacji Dog Shelter Manager. Testy pokrywają aspekty funkcjonalności API, takie jak: operacje CRUD, filtrowanie, sortowanie, działanie WebSockets oraz walidację danych.
### Struktura testów
1. `test_dogs.py` - Testy podstawowych operacji CRUD
- Testy tworzenia
- Testy pobierania
- Testy aktualizacji
- Testy usuwania

2. `test_ws.py` - Testy WebSocket
- Podstawowe testy WebSocket
- Testy aktualizacji przez WebSocket

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
