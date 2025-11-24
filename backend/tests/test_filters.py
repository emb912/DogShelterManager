from fastapi.testclient import TestClient
from app.main import app
from app.routers.dog import get_db
from .database_test import override_get_db, setup_test_db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def setup_module(module):
    setup_test_db()


def add_dog(name, size, status, birth_date="2020-01-01"):
    data = {
        "name": name,
        "size": size,
        "birth_date": birth_date,
        "sex": "male",
        "admitted_date": "2023-01-01",
        "released_date": None,
        "status": status,
        "neutered": True
    }
    client.post("/dogs/", json=data)


def test_filter_by_size():
    setup_test_db()
    add_dog("A", "small", "arrived")
    add_dog("B", "medium", "arrived")

    response = client.get("/dogs/?size=small")
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "A"


def test_sort_by_name_desc():
    setup_test_db()
    add_dog("Charlie", "small", "arrived")
    add_dog("Burek", "small", "arrived")

    response = client.get("/dogs/?sort_by=name&sort_order=desc")
    names = [d["name"] for d in response.json()]
    assert names == ["Charlie", "Burek"]
