import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.dog import get_db
from tests.database_test import override_get_db, setup_test_db, TestingSessionLocal
from datetime import date, timedelta

@pytest.fixture(autouse=True)
def run_before_tests():
    setup_test_db()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def run_before_each_test():
    setup_test_db()


# ============= TESTY TWORZENIA PSÓW =============

def test_create_dog():
    """Test podstawowego tworzenia psa"""
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
    assert result["sex"] == "male"
    assert result["neutered"] == True
    assert result["status"] == "arrived"
    assert "id" in result


def test_create_dog_minimal_data():
    """Test tworzenia psa z minimalnymi wymaganymi polami"""
    dog_data = {
        "name": "Burek",
        "size": "large",
        "birth_date": None,
        "sex": None,
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived"
    }

    response = client.post("/dogs/", json=dog_data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Burek"
    assert result["birth_date"] is None
    assert result["sex"] is None

def test_create_dog_invalid_size():
    """Test tworzenia psa z nieprawidłowym rozmiarem"""
    dog_data = {
        "name": "Test",
        "size": "extra_large",  # nieprawidłowy rozmiar
        "birth_date": "2021-01-01",
        "sex": "male",
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived"
    }
    response = client.post("/dogs/", json=dog_data)
    assert response.status_code == 422  # Validation error


def test_create_dog_invalid_status():
    """Test tworzenia psa z nieprawidłowym statusem"""
    dog_data = {
        "name": "Test",
        "size": "medium",
        "birth_date": "2021-01-01",
        "sex": "male",
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "escaped"  # nieprawidłowy status
    }
    response = client.post("/dogs/", json=dog_data)
    assert response.status_code == 422


# ============= TESTY POBIERANIA PSÓW =============

def test_get_dogs_list():
    """Test pobierania listy psów"""
    test_create_dog()

    response = client.get("/dogs/")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["name"] == "Reksio"


def test_get_empty_dogs_list():
    """Test pobierania pustej listy psów"""
    response = client.get("/dogs/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_single_dog():
    """Test pobierania pojedynczego psa po ID"""
    # Utwórz psa
    dog_data = {
        "name": "Azor",
        "size": "large",
        "birth_date": "2019-03-15",
        "sex": "male",
        "neutered": True,
        "admitted_date": "2023-06-01",
        "released_date": None,
        "status": "arrived"
    }
    create_response = client.post("/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]

    response = client.get(f"/dogs/{dog_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Azor"
    assert result["size"] == "large"
    assert result["id"] == dog_id


def test_get_non_existent_dog():
    """Test pobierania nieistniejącego psa"""
    response = client.get("/dogs/999")
    # zwraca None lub 404
    assert response.status_code in [200, 404] or response.json() is None


# ============= TESTY AKTUALIZACJI =============

def test_update_dog():
    """Test podstawowej aktualizacji psa"""
    test_create_dog()
    response = client.put("/dogs/1", json={"name": "Piesek"})
    assert response.status_code == 200

    result = response.json()
    assert result["name"] == "Piesek"


def test_update_dog_name():
    """Test aktualizacji tylko imienia"""
    dog_data = {
        "name": "Stare Imię",
        "size": "medium",
        "birth_date": "2020-05-10",
        "sex": "male",
        "admitted_date": "2023-11-01",
        "released_date": None,
        "status": "arrived",
        "neutered": True
    }
    create_response = client.post("/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]

    update_response = client.put(f"/dogs/{dog_id}", json={"name": "Nowe Imię"})
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["name"] == "Nowe Imię"
    assert result["size"] == "medium"  # inne pola się nie zmieniły


def test_update_dog_status():
    """Test aktualizacji statusu psa"""
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
    create_response = client.post("/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]

    # zmiana statusu na adopted
    update_response = client.put(f"/dogs/{dog_id}", json={
        "status": "adopted",
        "released_date": "2024-06-01"
    })
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["status"] == "adopted"
    assert result["released_date"] == "2024-06-01"


def test_update_dog_multiple_fields():
    """Test aktualizacji wielu pól naraz"""
    dog_data = {
        "name": "Rex",
        "size": "small",
        "birth_date": "2020-01-01",
        "sex": "male",
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived",
        "neutered": False
    }
    create_response = client.post("/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]

    update_data = {
        "name": "Rex Jr.",
        "size": "medium",
        "neutered": True,
        "status": "adopted"
    }
    update_response = client.put(f"/dogs/{dog_id}", json=update_data)
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["name"] == "Rex Jr."
    assert result["size"] == "medium"
    assert result["neutered"] == True
    assert result["status"] == "adopted"


def test_update_non_existent_dog():
    """Test aktualizacji nieistniejącego psa"""
    response = client.put("/dogs/9999", json={"name": "Test"})
    assert response.status_code == 404

def test_update_preserves_unmodified_fields():
    """Test że aktualizacja nie zmienia niewyszczególnionych pól"""
    dog_data = {
        "name": "Burek",
        "size": "large",
        "birth_date": "2019-05-15",
        "sex": "male",
        "admitted_date": "2023-01-01",
        "released_date": None,
        "status": "arrived",
        "neutered": True
    }
    create_response = client.post("/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]
    original = create_response.json()

    # Zaktualizuj tylko nazwę
    update_response = client.put(f"/dogs/{dog_id}", json={"name": "Burek Wielki"})
    updated = update_response.json()

    assert updated["name"] == "Burek Wielki"
    assert updated["size"] == original["size"]
    assert updated["birth_date"] == original["birth_date"]
    assert updated["sex"] == original["sex"]
    assert updated["admitted_date"] == original["admitted_date"]
    assert updated["neutered"] == original["neutered"]


# ============= TESTY USUWANIA =============

def test_delete_dog():
    """Test podstawowego usuwania psa"""
    test_create_dog()
    response = client.delete("/dogs/1")
    assert response.status_code == 200

    response = client.get("/dogs/")
    assert response.status_code == 200
    assert response.json() == []


def test_delete_non_existent_dog():
    """Test usuwania nieistniejącego psa"""
    response = client.delete("/dogs/9999")
    assert response.status_code == 404


def test_delete_dog_by_id():
    """Test usuwania konkretnego psa po ID"""
    # Utwórz kilka psów
    for i in range(3):
        dog_data = {
            "name": f"Pies_{i}",
            "size": "medium",
            "birth_date": "2020-01-01",
            "sex": "male",
            "admitted_date": "2024-01-01",
            "released_date": None,
            "status": "arrived",
            "neutered": False
        }
        client.post("/dogs/", json=dog_data)

    # usuwam środkowego psa (ID = 2)
    delete_response = client.delete("/dogs/2")
    assert delete_response.status_code == 200

    # sprawdzam, czy został usunięty
    get_response = client.get("/dogs/")
    assert len(get_response.json()) == 2
    ids = [dog["id"] for dog in get_response.json()]
    assert 2 not in ids


