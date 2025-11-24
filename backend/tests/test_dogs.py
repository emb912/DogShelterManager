import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.dog import get_db
from tests.database_test import override_get_db, setup_test_db, TestingSessionLocal

@pytest.fixture(autouse=True)
def run_before_tests():
    setup_test_db()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def run_before_each_test():
    setup_test_db()


def test_create_dog():
    dog_data = {
        "name": "Reksio",
        "size": "medium",
        "birth_date": "2020-05-10",
        "sex": "male",
        "admitted_date": "2023-11-01",
        "released_date": None,
        "status": "arrived",
        "neutered": True
    }

    response = client.post("/dogs/", json=dog_data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Reksio"
    assert result["size"] == "medium"


def test_get_dogs_list():
    # add dog
    test_create_dog()

    response = client.get("/dogs/")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["name"] == "Reksio"


def test_update_dog():
    # add dog
    test_create_dog()
    response = client.put("/dogs/1", json={"name": "Piesek"})
    assert response.status_code == 200

    result = response.json()
    print("LOL", result)
    assert result["name"] == "Piesek"


def test_delete_dog():
    test_create_dog()
    response = client.delete("/dogs/1")
    assert response.status_code == 200

    response = client.get("/dogs/")
    assert response.status_code == 200
    assert response.json() == []
