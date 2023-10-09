import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def categoria_for_test():
    response = client.post("/categorias/NuevaCategoria")
    return response.json()["id_categoria"]
id_cat = categoria_for_test()

def test_create_categoria():
    response = client.post("/categorias/NuevaCategoria")
    assert response.status_code == 200
    categoria = response.json()
    assert "id_categoria" in categoria
    assert categoria["nombre"] == "NuevaCategoria"

def test_get_categorias():
    response = client.get("/categorias/")
    assert response.status_code == 200
    categorias = response.json()
    assert isinstance(categorias, list)

def test_get_categoria_existente():
    response = client.get(f"/categorias/{id_cat}")
    assert response.status_code == 200
    categoria = response.json()
    assert "id_categoria" in categoria

def test_get_categoria_no_existente():
    response = client.get("/categorias/999")
    assert response.status_code == 404

def test_update_categoria_existente():
    response = client.put("/categorias/", json={"id_categoria": f"{id_cat}", "nombre": "NuevoNombre"})
    assert response.status_code == 200
    resultado = response.json()
    assert resultado["result"] == "Actualizado"

def test_update_categoria_no_existente():
    response = client.put("/categorias/", json={"id_categoria":'99', "nombre": "NuevoNombre"})
    assert response.status_code == 404

def test_delete_categoria_existente():
    response = client.delete(f"/categorias/{id_cat}")
    assert response.status_code == 200
    mensaje = response.json()
    assert mensaje["message"] == "Categoria eliminada"

def test_delete_categoria_no_existente():
    response = client.delete("/categorias/999")
    assert response.status_code == 404
