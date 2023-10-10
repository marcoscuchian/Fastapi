import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)



example_categoryclient = {
    "id_client": "example_client_id",
    "id_category": "example_category_id"
}

def test_create_category_client():
    create_client_response = client.post("/client/", json={"name": "Ejemplo de cliente"})
    assert create_client_response.status_code == 200
    client_data = create_client_response.json()
    example_categoryclient["id_client"] = client_data["id"]

    create_category_response = client.post("/categorys/", json={"name": "Ejemplo de categoría"})
    assert create_category_response.status_code == 200
    category_data = create_category_response.json()
    example_categoryclient["id_category"] = category_data["id"]

    response = client.post("/categorys_clients/", json=example_categoryclient)
    assert response.status_code == 200
    data = response.json()

def test_get_categorys_clients():
    response = client.get("/categorys_clients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_categorys_by_client():
    create_response = client.post("/categorys_clients/", json=example_categoryclient)
    assert create_response.status_code == 200

    response = client.get(f"/categorys_clients/category_by_client/{example_categoryclient['id_client']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_clients_by_id_category():
    create_response = client.post("/categorys_clients/", json=example_categoryclient)
    assert create_response.status_code == 200

    response = client.get(f"/categorys_clients/clients_by_category/{example_categoryclient['id_category']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

