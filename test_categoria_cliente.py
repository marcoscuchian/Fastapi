import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_categorias_clientes():
    response = client.get("/categorias_clientes/")
    assert response.status_code == 200
    categorias_clientes = response.json()
    assert isinstance(categorias_clientes, list)

def test_get_categorias_by_client_existente():
    response = client.get("/categorias_clientes/categoria_by_client/1")
    assert response.status_code == 200
    categorias = response.json()
    assert isinstance(categorias, list)

def test_get_categorias_by_client_no_existente():
    response = client.get("/categorias_clientes/categoria_by_client/999")
    assert response.status_code == 404

def test_get_clients_by_id_categoria_existente():
    response = client.get("/categorias_clientes/clients_by_categoria/1")
    assert response.status_code == 200
    clientes = response.json()
    assert isinstance(clientes, list)

def test_get_clients_by_id_categoria_no_existente():
    response = client.get("/categorias_clientes/clients_by_categoria/999")
    assert response.status_code == 404

def test_create_categoria_cliente_existente():
    response = client.post("/categorias_clientes/categorias_cliente/1/1")
    assert response.status_code == 200
    resultado = response.json()
    assert "id_cliente" in resultado
    assert "id_categoria" in resultado

def test_create_categoria_cliente_no_existente():
    response = client.post("/categorias_clientes/categorias_cliente/999/999")
    assert response.status_code == 404

def test_delete_categoria_cliente_existente():
    response = client.delete("/categorias_clientes/categoria_cliente/1/1")
    assert response.status_code == 200
    mensaje = response.json()
    assert mensaje["message"] == "Categoría eliminada"

def test_delete_categoria_cliente_no_existente():
    response = client.delete("/categorias_clientes/categoria_cliente/999/999")
    assert response.status_code == 404
