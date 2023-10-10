from fastapi import APIRouter
from config.db import conn
from fastapi import APIRouter, HTTPException, status
from models.models import motion , account
from schemas.motion import Motion
from datetime import datetime
from typing import List

mvnto = APIRouter(
    prefix= "/motions",
    tags=['Motions']
)


@mvnto.get('/', response_model=List[Motion])
def get_motions():
    result = conn.execute(motion.select()).fetchall()
    result = [{
        "id": row.id,
        "id_account": row.id_account,
        "type": row.type,
        "amount": row.amount,
        "date": row.date
    } for row in result]
    return result


@mvnto.get("/{id_motion}" )
def get_motions_by_id(id_motion: str):
    result = conn.execute(motion.select().where(motion.c.id == id_motion))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect motion identification")
    if result:
        result = [{
            "id": row.id,
            "id_account": row.id_account,
            "type": row.type,
            "amount": row.amount,
            "date": row.date
        } for row in result]
        return result


@mvnto.get("/motionsbyaccount/{id_account}" )
def get_motions_by_id_account(id_account: str):
    existing_account = conn.execute(account.select().where(account.c.id == id_account)).first()
    if not existing_account:
        raise HTTPException(status_code=404, detail="Incorrect Account")

    result = conn.execute(motion.select().where(motion.c.id_account == id_account))
    result = [{
        "id": row.id,
        "id_account": row.id_account,
        "type": row.type,
        "amount": row.amount,
        "date": row.date
    } for row in result]
    if not result:
        raise HTTPException(status_code=404, detail="Motions not found")
    return result


@mvnto.post("/")
def create_motion(new_motion : Motion ):
    new_motion.type = new_motion.type.lower()
    if new_motion.type not in ['egreso', 'ingreso']:
        raise HTTPException(status_code=400, detail="The 'type' field must be 'Egreso' or 'Ingreso")
    balance = conn.execute(account.select().where(account.c.id == new_motion.id_account)).first()
    if not balance:
        raise HTTPException(status_code=404, detail="Account not found")
    balance_actual = balance[2] if balance[2] is not None else 0
    if new_motion.type == 'egreso':
        if balance_actual < new_motion.amount:
            raise HTTPException(status_code=400, detail="You don't have enough balance")
        nuevo_balance = balance_actual - new_motion.amount
    else:
        nuevo_balance = balance_actual + new_motion.amount

    conn.execute(account.update().where(account.c.id == new_motion.id_account).values(balance=nuevo_balance))
    new_motion = {"id_account": new_motion.id_account, "type": new_motion.type, "amount": new_motion.amount, "date": datetime.now()}
    result = conn.execute(motion.insert().values(new_motion))
    new_motion["id"] = result.inserted_primary_key[0]
    conn.commit()
    return new_motion

@mvnto.delete("/{id_motion}")
def delete_motion(id_motion: str):
    result = conn.execute(motion.delete().where(motion.c.id == id_motion))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="id_motion not found")
    return {"message": "Motion removed"}



