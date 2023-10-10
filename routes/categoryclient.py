from fastapi import APIRouter
from config.db import conn
from schemas.categoryclient import Categoryclient
from fastapi import APIRouter, HTTPException
from typing import List

from models.models import categoryclient, client, category

catClien = APIRouter(
    prefix= "/categorys_clients",
    tags=['Categorys Clients']
)

@catClien.get('/', response_model=List[Categoryclient])
def get_categorys_clients():
    result = conn.execute(categoryclient.select()).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No categorys found")
    result = [{"id_client": row.id_client, "id_category": row.id_category} for row in result]
    return result

@catClien.get("/category_by_client/{id}" )
def get_categorys__by_client(id: str):
    result = conn.execute(categoryclient.select().where(categoryclient.c.id_client == id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="client not found")
    result = [{"id_client": row.id_client, "id_category": row.id_category} for row in result]
    return result

@catClien.get("/clients_by_category/{id_category}" )
def get_clients__by_id_category(id_category: str):
    result = conn.execute(categoryclient.select().where(categoryclient.c.id_category == id_category))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    result = [{"id_client": row.id_client, "id_category": row.id_category} for row in result]
    return result

@catClien.post("/",tags=['Categorys Clients'])
def create_category_client(new: Categoryclient):
    client_exists = conn.execute(client.select().where(client.c.id == new.id_client)).fetchone()
    category_exists = conn.execute(category.select().where(category.c.id == new.id_category)).fetchone()

    if not client_exists or not category_exists:
        raise HTTPException(status_code=404, detail="client o Category not found")
    new = {"id_category": new.id_category, "id_client": new.id_client}

    result = conn.execute(categoryclient.insert().values(new))
    conn.commit()


    return new

@catClien.delete("/")
def delete_category_client(new: Categoryclient):
    result = conn.execute(categoryclient.delete().where(
        categoryclient.c.id_client == new.id_client and categoryclient.c.id_category == new.id_category
    ))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Client or Category not found")
    return [{"message": "Category removed"}]
