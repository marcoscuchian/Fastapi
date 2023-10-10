from fastapi import APIRouter
from config.db import conn
from schemas.client import Clients
from fastapi import APIRouter, HTTPException, status
from models.models import client
from typing import List

clte = APIRouter(
    prefix= "/client",
    tags=['Clients']
)


@clte.get('/', response_model=List[Clients])
def get_client():
    clients_result = conn.execute(client.select()).fetchall()
    clients_result = [{"id": row.id, "name": row.name} for row in clients_result]
    return clients_result

@clte.get("/{id}" )
def get_client(id: str):
    result = conn.execute(client.select().where(client.c.id == id)).first()
    if result:
        user_client = {"id": result.id ,"name": result.name}
        return user_client
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")

@clte.post("/", response_model=Clients)
def create_client(client_data: Clients):
    new_client = {"name": client_data.name}
    try:
        result = conn.execute(client.insert().values(new_client))
        new_id = result.inserted_primary_key[0]
        new_client["id"] = new_id
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el client")
    return new_client

@clte.put("/update")
def update_client(client_data: Clients):
    existing_client = conn.execute(client.select().where(client.c.id == client_data.id)).first()
    if existing_client:
        try:
            conn.execute(client.update().values(name=client_data.name).where(client.c.id == client_data.id))
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el client")
        return {"message": "updated client", "id": client_data.id, "name": client_data.name}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")

@clte.delete("/{id}")
def delete_client(id: str):
    result = conn.execute(client.delete().where(client.c.id == id))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
    return [{"message": "client removed"}]
