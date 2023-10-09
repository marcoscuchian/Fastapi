from fastapi import APIRouter
from config.db import conn
from fastapi import APIRouter, HTTPException, status
from models.models import categoria
from schemas.categoria import Categoria
from typing import List

cat = APIRouter(
    prefix= "/categorias",
    tags=["Categorias"]
)

@cat.get('/', response_model=List[Categoria])
def get_categorias():
    categoria_result = conn.execute(categoria.select()).fetchall()

    if not categoria_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron categorías")

    categoria_result = [{"id_categoria": row.id_categoria, "nombre": row.nombre} for row in categoria_result]
    return categoria_result


@cat.get("/{id}")
def get_categoria(id: str):
    result = conn.execute(categoria.select().where(categoria.c.id_categoria == id)).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")

    user_categoria = {"id_categoria": result.id_categoria, "nombre": result.nombre}
    return user_categoria

@cat.post("/{nombre}", response_model=Categoria)
def create_categoria(nombre: str):
    new_categoria_data = {"nombre": nombre}
    try:
        result = conn.execute(categoria.insert().values(new_categoria_data))
        new_id = result.inserted_primary_key[0]
        new_categoria_data["id_categoria"] = new_id
        conn.commit()
        return new_categoria_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la categoría: {str(e)}")


@cat.put("/")
def update_categoria(new_categoria: Categoria):
    existing_categoria = conn.execute(categoria.select().where(categoria.c.id_categoria == new_categoria.id_categoria)).first()
    if existing_categoria:
        conn.execute(categoria.update().values(nombre=new_categoria.nombre).where(categoria.c.id_categoria == new_categoria.id_categoria))
        conn.commit()
        return {"result":"Actualizado"}
    else:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

@cat.delete("/{id_categoria}")
def delete_categoria(id_categoria: str):
    result = conn.execute(categoria.delete().where(categoria.c.id_categoria == id_categoria))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return {"message": "Categoria eliminada"}
