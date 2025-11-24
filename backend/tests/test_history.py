from fastapi.testclient import TestClient
from app.main import app
from app.routers.dog import get_db
from tests.database_test import override_get_db, setup_test_db, TestingSessionLocal
import pytest

@pytest.fixture(autouse=True)
def run_before_tests():
    setup_test_db()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_history_changes():
    # create dog
    dog = {
        "name": "Reksio",
        "size": "medium",
        "birth_date": "2020-05-10",
        "sex": "male",
        "admitted_date": "2023-11-01",
        "released_date": None,
        "status": "arrived",
        "neutered": True
    }

    client.post("/dogs/", json=dog)
    client.put("/dogs/1", json={"status": "adopted"})

    # get history
    history = client.get("/dog-history/1")
    assert history.status_code == 200
    items = history.json()
    assert len(items) >= 1
    assert items[0]["field_name"] == "status"
    assert items[0]["old_value"] == "DogStatus.arrived"
    assert items[0]["new_value"] == "DogStatus.adopted"
