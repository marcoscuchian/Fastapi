from fastapi import APIRouter
from config.db import conn
from schemas.categoriacliente import CategoriaCliente
from fastapi import APIRouter, HTTPException
from typing import List

from models.models import categoriaCliente, clientes, categoria

catClien = APIRouter(
    prefix= "/categorias_clientes",
    tags=['Categorias Clientes']
)

@catClien.get('/', response_model=List[CategoriaCliente])
def get_categorias_clientes():
    result = conn.execute(categoriaCliente.select()).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No se encontraron categorías")
    result = [{"id_cliente": row.id_cliente, "id_categoria": row.id_categoria} for row in result]
    return result



@catClien.get("/categoria_by_client/{id_cliente}" )
def get_categorias__by_client(id_cliente: str):
    result = conn.execute(categoriaCliente.select().where(categoriaCliente.c.id_cliente == id_cliente))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    result = [{"id_cliente": row.id_cliente, "id_categoria": row.id_categoria} for row in result]
    return result


@catClien.get("/clients_by_categoria/{id_categoria}" )
def get_clients__by_id_categoria(id_categoria: str):
    result = conn.execute(categoriaCliente.select().where(categoriaCliente.c.id_categoria == id_categoria))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    result = [{"id_cliente": row.id_cliente, "id_categoria": row.id_categoria} for row in result]
    return result

@catClien.post("/categorias_cliente/{id_client}/{id_categoria}",tags=['Categorias Clientes'])
def create_categoria_cliente(id_client: str ,id_categoria:str):
    client_exists = conn.execute(clientes.select().where(clientes.c.id_cliente == id_client)).fetchone()
    categoria_exists = conn.execute(categoria.select().where(categoria.c.id_categoria == id_categoria)).fetchone()

    if not client_exists or not categoria_exists:
        raise HTTPException(status_code=404, detail="Cliente o categoría no encontrada")
    new = {"id_cliente": id_client, "id_categoria": id_categoria}

    try:
        result = conn.execute(categoriaCliente.insert().values(new))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear la categoría del cliente")

    return new


@catClien.delete("/categoria_cliente/{id_client}/{id_categoria}")
def delete_categoria_cliente(id_client: str, id_categoria: str):
    result = conn.execute(categoriaCliente.delete().where(
        categoriaCliente.c.id_cliente == id_client and categoriaCliente.c.id_categoria == id_categoria
    ))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cliente o categoría no encontrados")
    return {"message": "Categoría eliminada"}
