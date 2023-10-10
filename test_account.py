import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def id_test_create_client():
    data = {"id": "", "name": "Nuevoclient"}
    response = client.post("/client", json=data)
    return response.json()

client_info = id_test_create_client()
client_test = client_info["id"]

example_account = {
    "id_client": client_test
}

def test_create_account():
    create_client_response = client.post("/client/", json={"name": "Ejemplo de cliente"})
    assert create_client_response.status_code == 200
    client_data = create_client_response.json()
    example_account["id_client"] = client_data["id"]

    response = client.post("/accounts/", json=example_account)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

def test_get_accounts():
    response = client.get("/accounts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_accounts_by_client():
    create_response = client.post("/accounts/", json=example_account)
    assert create_response.status_code == 200
    created_data = create_response.json()
    account_id = created_data["id"]

    response = client.get(f"/accounts/accounts_by_client/{example_account['id_client']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_accounts_by_id():
    create_response = client.post("/accounts/", json=example_account)
    assert create_response.status_code == 200
    created_data = create_response.json()
    account_id = created_data["id"]

    response = client.get(f"/accounts/{account_id}")
    assert response.status_code == 200


def test_get_total_usd():
    create_response = client.post("/accounts/", json=example_account)
    assert create_response.status_code == 200
    created_data = create_response.json()
    account_id = created_data["id"]

    response = client.get(f"/accounts/get_total_usd/{account_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_delete_account():
    create_response = client.post("/accounts/", json=example_account)
    assert create_response.status_code == 200
    created_data = create_response.json()
    account_id = created_data["id"]

    response = client.delete(f"/accounts/{account_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Account removed"}

    get_response = client.get(f"/accounts/{account_id}")
    assert get_response.status_code == 404
