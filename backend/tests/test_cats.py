import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.cat import get_db
from tests.database_test import override_get_db, setup_test_db, TestingSessionLocal

@pytest.fixture(autouse=True)
def run_before_tests():
    setup_test_db()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def run_before_each_test():
    setup_test_db()


def test_create_cat():
    """Test podstawowego tworzenia kota"""
    cat_data = {
        "name": "Mruczek",
        "size": "medium",
        "indoor_only": True,
        "birth_date": "2020-05-10",
        "sex": "male",
        "neutered": True,
        "admitted_date": "2023-11-01",
        "released_date": None,
        "status": "arrived",
    }

    response = client.post("/cats/", json=cat_data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Mruczek"
    assert result["size"] == "medium"
    assert result["indoor_only"] is True
    assert result["status"] == "arrived"
    assert "id" in result


def test_create_cat_minimal_data():
    """Test tworzenia kota z minimalnymi wymaganymi polami"""
    cat_data = {
        "name": "Filemon",
        "size": "small",
        "indoor_only": False,
        "birth_date": None,
        "sex": None,
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived",
    }

    response = client.post("/cats/", json=cat_data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Filemon"
    assert result["birth_date"] is None
    assert result["sex"] is None


def test_create_cat_invalid_size():
    """Test tworzenia kota z nieprawidłowym rozmiarem"""
    cat_data = {
        "name": "Test",
        "size": "giant",  # nieprawidłowy rozmiar
        "indoor_only": False,
        "birth_date": "2021-01-01",
        "sex": "female",
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived",
    }
    response = client.post("/cats/", json=cat_data)
    assert response.status_code == 422  # Validation error


def test_create_cat_invalid_status():
    """Test tworzenia kota z nieprawidłowym statusem"""
    cat_data = {
        "name": "Test",
        "size": "medium",
        "indoor_only": False,
        "birth_date": "2021-01-01",
        "sex": "female",
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "lost",  # nieprawidłowy status
    }
    response = client.post("/cats/", json=cat_data)
    assert response.status_code == 422


def test_get_cats_list():
    """Test pobierania listy kotów"""
    test_create_cat()

    response = client.get("/cats/")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["name"] == "Mruczek"


def test_get_empty_cats_list():
    """Test pobierania pustej listy kotów"""
    response = client.get("/cats/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_single_cat():
    """Test pobierania pojedynczego kota po ID"""
    cat_data = {
        "name": "Puszek",
        "size": "large",
        "indoor_only": True,
        "birth_date": "2019-03-15",
        "sex": "male",
        "neutered": True,
        "admitted_date": "2023-06-01",
        "released_date": None,
        "status": "arrived",
    }
    create_response = client.post("/cats/", json=cat_data)
    cat_id = create_response.json()["id"]

    response = client.get(f"/cats/{cat_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Puszek"
    assert result["size"] == "large"
    assert result["id"] == cat_id


def test_get_non_existent_cat():
    """Test pobierania nieistniejącego kota"""
    response = client.get("/cats/999")
    assert response.status_code == 404


def test_update_cat():
    """Test podstawowej aktualizacji kota"""
    test_create_cat()
    response = client.put("/cats/1", json={"name": "Kotek"})
    assert response.status_code == 200

    result = response.json()
    assert result["name"] == "Kotek"


def test_update_cat_name():
    """Test aktualizacji tylko imienia kota"""
    cat_data = {
        "name": "Stare Imię",
        "size": "medium",
        "indoor_only": False,
        "birth_date": "2020-05-10",
        "sex": "female",
        "neutered": False,
        "admitted_date": "2023-11-01",
        "released_date": None,
        "status": "arrived",
    }
    create_response = client.post("/cats/", json=cat_data)
    cat_id = create_response.json()["id"]

    update_response = client.put(f"/cats/{cat_id}", json={"name": "Nowe Imię"})
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["name"] == "Nowe Imię"
    assert result["size"] == "medium"  # inne pola się nie zmieniły


def test_update_cat_status():
    """Test aktualizacji statusu kota"""
    cat_data = {
        "name": "Mruczek",
        "size": "large",
        "indoor_only": True,
        "birth_date": "2020-01-01",
        "sex": "male",
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived",
    }
    create_response = client.post("/cats/", json=cat_data)
    cat_id = create_response.json()["id"]

    update_response = client.put(f"/cats/{cat_id}", json={
        "status": "adopted",
        "released_date": "2024-06-01",
    })
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["status"] == "adopted"
    assert result["released_date"] == "2024-06-01"


def test_update_cat_multiple_fields():
    """Test aktualizacji wielu pól kota naraz"""
    cat_data = {
        "name": "Klakier",
        "size": "small",
        "indoor_only": False,
        "birth_date": "2020-01-01",
        "sex": "male",
        "neutered": False,
        "admitted_date": "2024-01-01",
        "released_date": None,
        "status": "arrived",
    }
    create_response = client.post("/cats/", json=cat_data)
    cat_id = create_response.json()["id"]

    update_data = {
        "name": "Klakier Jr.",
        "size": "medium",
        "indoor_only": True,
        "status": "adopted",
    }
    update_response = client.put(f"/cats/{cat_id}", json=update_data)
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["name"] == "Klakier Jr."
    assert result["size"] == "medium"
    assert result["indoor_only"] is True
    assert result["status"] == "adopted"


def test_update_non_existent_cat():
    """Test aktualizacji nieistniejącego kota"""
    response = client.put("/cats/9999", json={"name": "Test"})
    assert response.status_code == 404


def test_update_preserves_unmodified_fields_cat():
    """Test że aktualizacja nie zmienia niewyszczególnionych pól kota"""
    cat_data = {
        "name": "Filemon",
        "size": "large",
        "indoor_only": True,
        "birth_date": "2019-05-15",
        "sex": "male",
        "neutered": True,
        "admitted_date": "2023-01-01",
        "released_date": None,
        "status": "arrived",
    }
    create_response = client.post("/cats/", json=cat_data)
    cat_id = create_response.json()["id"]
    original = create_response.json()

    update_response = client.put(f"/cats/{cat_id}", json={"name": "Filemon Wielki"})
    updated = update_response.json()

    assert updated["name"] == "Filemon Wielki"
    assert updated["size"] == original["size"]
    assert updated["birth_date"] == original["birth_date"]
    assert updated["sex"] == original["sex"]
    assert updated["status"] == original["status"]


def test_delete_cat():
    """Test usuwania kota"""
    test_create_cat()

    response = client.delete("/cats/1")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}

    get_response = client.get("/cats/1")
    assert get_response.status_code == 404


def test_delete_non_existent_cat():
    """Test usuwania nieistniejącego kota"""
    response = client.delete("/cats/9999")
    assert response.status_code == 404
