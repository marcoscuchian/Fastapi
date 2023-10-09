from fastapi import APIRouter
from config.db import conn
from schemas.cuenta import Cuenta
from fastapi import APIRouter, HTTPException, status
import requests

from models.models import cuenta

cnta = APIRouter(
    prefix= "/cuentas",
    tags=['Cuentas']
)

@cnta.get('/')
def get_cuentas():
    cuenta_result = conn.execute(cuenta.select()).fetchall()
    if not cuenta_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron cuentas")

    cuenta_result = [{"id_cuenta": row.id_cuenta, "id_cliente": row.id_cliente, "saldo" : row.saldo} for row in cuenta_result]
    return cuenta_result

@cnta.get("/cuentas_by_client/{id_client}" )
def get_cuentas_by_client(id_client: str):
    result = conn.execute(cuenta.select().where(cuenta.c.id_cliente == id_client))
    cuentas = [{"id_cliente": row.id_cliente, "id_cuenta": row.id_cuenta, 'saldo': row.saldo} for row in result]
    if cuentas:
        return cuentas
    else:
        raise HTTPException(status_code=404, detail="Cliente no tiene cuentas asociadas")

@cnta.get("/{id_cuenta}" )
def get_cuentas_by_id(id_cuenta: str):
    result = conn.execute(cuenta.select().where(cuenta.c.id_cuenta == id_cuenta))
    cuentas = [{"id_cliente": row.id_cliente, "id_cuenta": row.id_cuenta, 'saldo': row.saldo} for row in result]
    if cuentas:
        return cuentas
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")

@cnta.get("/get_total_usd/{id_cuenta}" )
def get_total_usd(id_cuenta: str):


    result = conn.execute(cuenta.select().where(cuenta.c.id_cuenta == id_cuenta)).fetchall()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    saldo = result[0][2] if result and result[0][2] is not None else 0

    url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
    response = requests.get(url)
    if response.status_code == 200:
        data_dolar = response.json()
        saldo_dolar = {'saldo_pesos' : saldo}
        monedas_a_calcular = ['Dolar Oficial', 'Dolar Blue', 'Dolar Soja', 'Dolar Contado con Liqui', 'Dolar Bolsa']
        for data in data_dolar:
            casa = data['casa']
            nombre = casa.get('nombre', '')
            if nombre in monedas_a_calcular and 'compra' in casa and casa['compra'] != 'No Cotiza':
                compra = float(casa['compra'].replace(",", "."))
                nombre = nombre.replace(" ", "_")
                saldo_dolar[nombre] = round(saldo / compra, 2)
        return [saldo_dolar]
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Error en la solicitud. Código de estado: {response.status_code}")

@cnta.post("/{id_client}", response_model=Cuenta)
def create_cuenta(id_client: str):
    new = {"id_cliente": id_client}
    result = conn.execute(cuenta.insert().values(new))
    new_id = result.inserted_primary_key[0]
    new["id_cuenta"] = new_id
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la cuenta")
    return new

@cnta.delete("/{id_cuenta}")
def delete_cuenta(id_cuenta: str):
    result = conn.execute(cuenta.delete().where(cuenta.c.id_cuenta == id_cuenta))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="cliente no encontrado")
    return {"message": "cliente eliminado"}
