from fastapi import APIRouter
from config.db import conn
from schemas.cliente import Cliente
from fastapi import APIRouter, HTTPException, status
from models.models import clientes
from typing import List

clte = APIRouter(
    prefix= "/clientes",
    tags=['Clientes']
)


@clte.get('/', response_model=List[Cliente])
def get_clientes():
    clientes_result = conn.execute(clientes.select()).fetchall()
    clientes_result = [{"id_cliente": row.id_cliente, "nombre": row.nombre} for row in clientes_result]
    return clientes_result

@clte.get("/{id}" )
def get_cliente(id: str):
    result = conn.execute(clientes.select().where(clientes.c.id_cliente == id)).first()
    if result:
        user_cliente = {"id_cliente": result.id_cliente ,"nombre": result.nombre}
        return user_cliente
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@clte.post("/", response_model=Cliente)
def create_cliente(cliente_data: Cliente):
    new_cliente = {"nombre": cliente_data.nombre}
    try:
        result = conn.execute(clientes.insert().values(new_cliente))
        new_id = result.inserted_primary_key[0]
        new_cliente["id_cliente"] = new_id
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el cliente")
    return new_cliente

@clte.put("/update")
def update_cliente(cliente_data: Cliente):
    existing_cliente = conn.execute(clientes.select().where(clientes.c.id_cliente == cliente_data.id_cliente)).first()
    if existing_cliente:
        try:
            conn.execute(clientes.update().values(nombre=cliente_data.nombre).where(clientes.c.id_cliente == cliente_data.id_cliente))
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el cliente")
        return {"message": "Cliente actualizado", "id_cliente": cliente_data.id_cliente, "nombre": cliente_data.nombre}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@clte.delete("/{cliente_id}")
def delete_cliente(cliente_id: str):
    result = conn.execute(clientes.delete().where(clientes.c.id_cliente == cliente_id))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return [{"message": "Cliente eliminado"}]
