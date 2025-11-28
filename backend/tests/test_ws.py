import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.dog import get_db
from tests.database_test import override_get_db, setup_test_db
import json
import time

@pytest.fixture(autouse=True)
def run_before_tests():
    setup_test_db()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup():
    setup_test_db()


# ============= TESTY WEBSOCKET - PODSTAWOWE =============

def test_websocket_connection():
    """Test podstawowego połączenia WebSocket"""
    with client.websocket_connect("/ws/dogs") as websocket:
        # Otrzymaj początkowe statystyki
        data = websocket.receive_json()
        assert "current_in_shelter" in data
        assert "adopted_total" in data
        assert "returned_total" in data
        assert "all_dogs_total" in data


def test_websocket_initial_stats_empty():
    """Test początkowych statystyk dla pustej bazy"""
    with client.websocket_connect("/ws/dogs") as websocket:
        stats = websocket.receive_json()
        assert stats["current_in_shelter"] == 0
        assert stats["adopted_total"] == 0
        assert stats["returned_total"] == 0
        assert stats["all_dogs_total"] == 0


def test_websocket_stats_after_add():
    """Test aktualizacji statystyk po dodaniu psa"""
    with client.websocket_connect("/ws/dogs") as websocket:
        # początkowe statystyki
        initial_stats = websocket.receive_json()
        
        # dodaje psa
        dog = {
            "name": "Rex",
            "size": "medium",
            "birth_date": "2020-05-10",
            "sex": "male",
            "admitted_date": "2023-01-01",
            "released_date": None,
            "status": "arrived",
            "neutered": True
        }
        client.post("/dogs/", json=dog)

        # odbieram zaktualizowane statystyki
        stats = websocket.receive_json()
        assert stats["current_in_shelter"] == 1
        assert stats["all_dogs_total"] == 1


def test_websocket_stats_multiple_dogs():
    """Test statystyk z wieloma psami o różnych statusach"""
    with client.websocket_connect("/ws/dogs") as websocket:
        websocket.receive_json()  # początkowe statystyki

        # dodaje psy z różnymi statusami
        dogs = [
            {"name": "Rex", "status": "arrived"},
            {"name": "Luna", "status": "arrived"},
            {"name": "Max", "status": "adopted"},
            {"name": "Bella", "status": "adopted"},
            {"name": "Charlie", "status": "returned"},
        ]

        for dog_data in dogs:
            full_data = {
                **dog_data,
                "size": "medium",
                "birth_date": "2020-01-01",
                "sex": "male",
                "admitted_date": "2024-01-01",
                "released_date": "2024-06-01" if dog_data["status"] != "arrived" else None,
                "neutered": False
            }
            client.post("/dogs/", json=full_data)
            stats = websocket.receive_json()

        # sprawdzam końcowe statystyki
        assert stats["current_in_shelter"] == 2  # arrived
        assert stats["adopted_total"] == 2
        assert stats["returned_total"] == 1
        assert stats["all_dogs_total"] == 5


# ============= TESTY WEBSOCKET - AKTUALIZACJE =============
def test_websocket_stats_after_update():
    """Test aktualizacji statystyk po zmianie statusu psa"""
    # Dodaje psa
    dog_data = {
        "name": "Azor",
        "size": "large",
        "birth_date": "2020-01-01",
        "sex": "male",
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived",
        "neutered": False
    }
    response = client.post("/dogs/", json=dog_data)
    dog_id = response.json()["id"]

    with client.websocket_connect("/ws/dogs") as websocket:
        initial = websocket.receive_json()
        assert initial["current_in_shelter"] == 1
        assert initial["adopted_total"] == 0

        # zmieniam status na adopted
        client.put(f"/dogs/{dog_id}", json={
            "status": "adopted",
            "released_date": "2024-06-01"
        })

        updated = websocket.receive_json()
        assert updated["current_in_shelter"] == 0
        assert updated["adopted_total"] == 1


def test_websocket_stats_after_delete():
    """Test aktualizacji statystyk po usunięciu psa"""
    # Dodaje psa
    dog_data = {
        "name": "Burek",
        "size": "medium",
        "birth_date": "2020-01-01",
        "sex": "male",
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived",
        "neutered": False
    }
    response = client.post("/dogs/", json=dog_data)
    dog_id = response.json()["id"]

    with client.websocket_connect("/ws/dogs") as websocket:
        initial = websocket.receive_json()
        assert initial["all_dogs_total"] == 1

        # usuwam psa
        client.delete(f"/dogs/{dog_id}")

        updated = websocket.receive_json()
        assert updated["all_dogs_total"] == 0
        assert updated["current_in_shelter"] == 0


def test_websocket_multiple_updates():
    """Test wielokrotnych aktualizacji statystyk"""
    with client.websocket_connect("/ws/dogs") as websocket:
        websocket.receive_json()  # początkowe

        # dodaje 3 psy
        for i in range(3):
            dog = {
                "name": f"Dog_{i}",
                "size": "medium",
                "birth_date": "2020-01-01",
                "sex": "male",
                "admitted_date": "2024-01-01",
                "released_date": None,
                "status": "arrived",
                "neutered": False
            }
            client.post("/dogs/", json=dog)
            stats = websocket.receive_json()

        assert stats["current_in_shelter"] == 3
        assert stats["all_dogs_total"] == 3


# ============= TESTY WEBSOCKET - WIELE POŁĄCZEŃ =============

def test_multiple_websocket_connections():
    """Test wielu jednoczesnych połączeń WebSocket"""
    with client.websocket_connect("/ws/dogs") as ws1:
        with client.websocket_connect("/ws/dogs") as ws2:
            # oba połączenia powinny dostaja początkowe statystyki
            stats1 = ws1.receive_json()
            stats2 = ws2.receive_json()
            
            assert stats1 == stats2
            assert stats1["all_dogs_total"] == 0

            # dodaje psa
            dog = {
                "name": "Rex",
                "size": "medium",
                "birth_date": "2020-01-01",
                "sex": "male",
                "admitted_date": "2024-01-01",
                "released_date": None,
                "status": "arrived",
                "neutered": False
            }
            client.post("/dogs/", json=dog)

            # oba połączenia powinny otrzymać aktualizację
            updated1 = ws1.receive_json()
            updated2 = ws2.receive_json()
            
            assert updated1 == updated2
            assert updated1["all_dogs_total"] == 1
