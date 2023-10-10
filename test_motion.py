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
    "id_client":client_test
}

response = client.post("/accounts", json=example_account)

id_acoounts = response.json()["id"]

example_motion = {
    "id_account": id_acoounts,
    "type": "ingreso",
    "amount": 50
}

def test_create_motion():
    response = client.post("/motions/", json=example_motion)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

def test_get_motions():
    response = client.get("/motions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_motion_by_id():
    create_response = client.post("/motions", json=example_motion)
    assert create_response.status_code == 200
    created_data = create_response.json()
    motion_id = created_data["id"]

    response = client.get(f"/motions/{motion_id}")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == motion_id

def test_get_motions_by_account():
    create_response = client.post("/motions/", json=example_motion)
    assert create_response.status_code == 200
    created_data = create_response.json()
    motion_id = created_data["id"]

    response = client.get(f"/motions/motionsbyaccount/{example_motion['id_account']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_delete_motion():
    create_response = client.post("/motions/", json=example_motion)
    assert create_response.status_code == 200
    created_data = create_response.json()
    motion_id = created_data["id"]

    response = client.delete(f"/motions/{motion_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Motion removed"}

    get_response = client.get(f"/motions/{motion_id}")
    assert get_response.status_code == 404