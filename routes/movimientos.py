from fastapi import APIRouter
from config.db import conn
from fastapi import APIRouter, HTTPException, status
from models.models import movimiento , cuenta
from schemas.movimiento import Movimiento
from datetime import datetime
from typing import List

mvnto = APIRouter(
    prefix= "/movimientos",
    tags=['Movimientos']
)


@mvnto.get('/', response_model=List[Movimiento])
def get_movimientos():
    try:
        result = conn.execute(movimiento.select()).fetchall()
        result = [{
            "id_movimiento": row.id_movimiento,
            "id_cuenta": row.id_cuenta,
            "tipo": row.tipo,
            "importe": row.importe,
            "fecha": row.fecha
        } for row in result]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@mvnto.get("/{id_movimiento}" )
def get_movimientos_by_id(id_movimiento: str):
    result = conn.execute(movimiento.select().where(movimiento.c.id_movimiento == id_movimiento))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id de movimiento incorrecto")
    if result:
        result = [{
            "id_movimiento": row.id_movimiento,
            "id_cuenta": row.id_cuenta,
            "tipo": row.tipo,
            "importe": row.importe,
            "fecha": row.fecha
        } for row in result]
        return result


@mvnto.get("/movimientosbycuenta/{id_cuenta}" )
def get_movimientos_by_id_cuenta(id_cuenta: str):
    existing_cuenta = conn.execute(cuenta.select().where(cuenta.c.id_cuenta == id_cuenta)).first()
    if not existing_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta incorrrecta")

    result = conn.execute(movimiento.select().where(movimiento.c.id_cuenta == id_cuenta))
    result = [{
        "id_movimiento": row.id_movimiento,
        "id_cuenta": row.id_cuenta,
        "tipo": row.tipo,
        "importe": row.importe,
        "fecha": row.fecha
    } for row in result]
    if not result:
        raise HTTPException(status_code=404, detail="Movimientos no encontrados")
    return result


@mvnto.post("/{id_cuenta}/{tipo}/{importe}")
def create_movimiento(id_cuenta: str, tipo: str, importe: int):
    tipo = tipo.lower()
    if tipo not in ['egreso', 'ingreso']:
        raise HTTPException(status_code=400, detail="El campo 'tipo' debe ser 'egreso' o 'ingreso'")
    saldo = conn.execute(cuenta.select().where(cuenta.c.id_cuenta == id_cuenta)).first()
    if not saldo:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    saldo_actual = saldo[2] if saldo[2] is not None else 0
    if tipo == 'egreso':
        if saldo_actual < importe:
            raise HTTPException(status_code=400, detail="No tienes suficiente saldo")
        nuevo_saldo = saldo_actual - importe
    else:
        nuevo_saldo = saldo_actual + importe

    conn.execute(cuenta.update().where(cuenta.c.id_cuenta == id_cuenta).values(saldo=nuevo_saldo))
    new_movimiento = {"id_cuenta": id_cuenta, "tipo": tipo, "importe": importe, "fecha": datetime.now()}
    result = conn.execute(movimiento.insert().values(new_movimiento))
    new_movimiento["id_movimiento"] = result.inserted_primary_key[0]
    conn.commit()
    return new_movimiento

@mvnto.delete("/{id_movimiento}")
def delete_movimiento(id_movimiento: str):
    result = conn.execute(movimiento.delete().where(movimiento.c.id_movimiento == id_movimiento))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="id_movimiento no encontrado")
    return {"message": "Movimiento eliminado"}



