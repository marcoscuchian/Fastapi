import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def id_test_create_cliente():
    data = {"id_cliente": "", "nombre": "NuevoCliente"}
    response = client.post("/clientes", json=data)
    return response.json()

cliente_info = id_test_create_cliente()
client_test = cliente_info["id_cliente"]


def test_get_clientes():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_cliente_existente():
    response = client.get(f"/clientes/{client_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_cliente_no_existente():
    response = client.get("/clientes/999")
    assert response.status_code == 404

def test_create_cliente():
    data = {"id_cliente": "", "nombre": "NuevoCliente"}
    response = client.post("/clientes", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_cliente_existente():
    data = {"id_cliente":f"{client_test}", "nombre": "NombreActualizado"}
    response = client.put("/clientes/update", json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_cliente_no_existente():
    data = {"id_cliente":"b7d4bcsss98e0-c3935be632ac", "nombre": "NombreActualizado"}
    response = client.put("/clientes/update", json=data)
    assert response.status_code == 404

def test_delete_cliente_existente():
    response = client.delete(f"/clientes/{client_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_cliente_no_existente():
    response = client.delete("/clientes/999")
    assert response.status_code == 404
