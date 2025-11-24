import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.dog import get_db
from tests.database_test import override_get_db, setup_test_db

@pytest.fixture(autouse=True)
def run_before_tests():
    setup_test_db()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup():
    setup_test_db()


def test_websocket_stats():
    with client.websocket_connect("/ws/dogs") as websocket:
        # add dog
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

        # receive stats
        stats = websocket.receive_json()
        assert stats["current_in_shelter"] == 1
