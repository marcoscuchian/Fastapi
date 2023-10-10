import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

example_category = {
    "name": "Ejemplo de categoría"
}

def test_create_category():
    response = client.post("/categorys/", json=example_category)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == example_category["name"]

def test_get_categorys():
    response = client.get("/categorys/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_category():
    # Crear una categoría de ejemplo primero
    create_response = client.post("/categorys/", json=example_category)
    assert create_response.status_code == 200
    created_data = create_response.json()
    category_id = created_data["id"]

    # Luego, obtener la categoría por su ID
    response = client.get(f"/categorys/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == example_category["name"]

def test_update_category():
    # Crear una categoría de ejemplo primero
    create_response = client.post("/categorys/", json=example_category)
    assert create_response.status_code == 200
    created_data = create_response.json()
    category_id = created_data["id"]

    # Actualizar la categoría
    updated_category = {"id": category_id, "name": "Nueva categoría"}
    response = client.put("/categorys/", json=updated_category)
    assert response.status_code == 200
    data = response.json()
    assert data == {"result": "Updated"}

    # Obtener la categoría actualizada
    get_response = client.get(f"/categorys/{category_id}")
    assert get_response.status_code == 200
    updated_data = get_response.json()
    assert updated_data["name"] == "Nueva categoría"

def test_delete_category():
    # Crear una categoría de ejemplo primero
    create_response = client.post("/categorys/", json=example_category)
    assert create_response.status_code == 200
    created_data = create_response.json()
    category_id = created_data["id"]

    # Luego, eliminar la categoría por su ID
    response = client.delete(f"/categorys/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Category removed"}

    # Intentar obtener la categoría nuevamente debería devolver un 404
    get_response = client.get(f"/categorys/{category_id}")
    assert get_response.status_code == 404
