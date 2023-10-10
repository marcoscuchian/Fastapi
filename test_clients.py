import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def id_test_create_client():
    data = {"id": "", "name": "Nuevoclient"}
    response = client.post("/client", json=data)
    return response.json()

client_info = id_test_create_client()
client_test = client_info["id"]


def test_get_clients():
    response = client.get("/client")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_client_existente():
    response = client.get(f"/client/{client_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_client_no_existente():
    response = client.get("/client/999")
    assert response.status_code == 404

def test_create_client():
    data = {"id": "", "name": "Nuevoclient"}
    response = client.post("/client", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_client_existente():
    data = {"id":f"{client_test}", "name": "NombreUpdated"}
    response = client.put("/client/update", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_client_no_existente():
    data = {"id":"b7d4bcsss98e0-c3935be632ac", "name": "NombreUpdated"}
    response = client.put("/client/update", json=data)
    assert response.status_code == 404

def test_delete_client_existente():
    response = client.delete(f"/client/{client_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_client_no_existente():
    response = client.delete("/client/999")
    assert response.status_code == 404
