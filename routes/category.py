from fastapi import APIRouter
from config.db import conn
from fastapi import APIRouter, HTTPException, status
from models.models import category
from schemas.category import Category
from typing import List

cat = APIRouter(
    prefix= "/categorys",
    tags=["Categorys"]
)

@cat.get('/', response_model=List[Category])
def get_categorys():
    category_result = conn.execute(category.select()).fetchall()

    if not category_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron Categorys")

    category_result = [{"id": row.id, "name": row.name} for row in category_result]
    return category_result


@cat.get("/{id}")
def get_category(id: str):
    result = conn.execute(category.select().where(category.c.id == id)).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    user_category = {"id": result.id, "name": result.name}
    return user_category

@cat.post("/", response_model=Category)
def create_category(name: Category):
    new_category_data = {"name": name.name}
    try:
        result = conn.execute(category.insert().values(new_category_data))
        new_id = result.inserted_primary_key[0]
        new_category_data["id"] = new_id
        conn.commit()
        return new_category_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating category:{str(e)}")


@cat.put("/")
def update_category(new_category: Category):
    existing_category = conn.execute(category.select().where(category.c.id == new_category.id)).first()
    if existing_category:
        conn.execute(category.update().values(name=new_category.name).where(category.c.id == new_category.id))
        conn.commit()
        return {"result":"Updated"}
    else:
        raise HTTPException(status_code=404, detail="Category not found")

@cat.delete("/{id}")
def delete_category(id: str):
    result = conn.execute(category.delete().where(category.c.id == id))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category removed"}
