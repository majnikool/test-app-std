# tests/test_main.py
from fastapi.testclient import TestClient
from app import crud, schemas

def test_create_item(client):
    response = client.post(
        "/items/",
        json={"name": "test item", "description": "test description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test item"
    assert data["description"] == "test description"
    assert "id" in data

def test_read_item(client):
    # First create an item
    response = client.post(
        "/items/",
        json={"name": "test item", "description": "test description"},
    )
    created_item = response.json()
    
    # Then read it
    response = client.get(f"/items/{created_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == created_item["name"]
    assert data["description"] == created_item["description"]