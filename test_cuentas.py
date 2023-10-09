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

def id_test_create_cuenta():
    response = client.post(f"/cuentas/{client_test}")
    return response.json()

cuenta_test = id_test_create_cuenta()["id_cuenta"]

def test_create_cuenta():
    response = client.post(f"/cuentas/{client_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_cuentas():
    response = client.get("/cuentas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_cuentas_by_client():
    response = client.get(f"/cuentas/cuentas_by_client/{client_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_cuentas_by_id():
    response = client.get(f"/cuentas/{cuenta_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_total_usd():
    response = client.get(f"/cuentas/get_total_usd/{cuenta_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_cuenta():
    response = client.delete(f"/cuentas/{cuenta_test}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)