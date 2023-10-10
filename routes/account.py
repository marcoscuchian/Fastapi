from fastapi import APIRouter
from config.db import conn
from schemas.account import Account
from schemas.client import Clients
from fastapi import APIRouter, HTTPException, status
import requests

from models.models import account, client

cnta = APIRouter(
    prefix= "/accounts",
    tags=['Accounts']
)

@cnta.get('/')
def get_accounts():
    account_result = conn.execute(account.select()).fetchall()
    if not account_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No accounts found")

    account_result = [{"id": row.id, "id_clent": row.id_client, "balance" : row.balance} for row in account_result]
    return account_result

@cnta.get("/accounts_by_client/{id_client}" )
def get_accounts_by_client(id_client: str):
    result = conn.execute(account.select().where(account.c.id_client == id_client))
    accounts = [{"id_client": row.id_client, "id": row.id, 'balance': row.balance} for row in result]
    if accounts:
        return accounts
    else:
        raise HTTPException(status_code=404, detail="client does not have associated accounts")

@cnta.get("/{id_account}" )
def get_accounts_by_id(id_account: str):
    result = conn.execute(account.select().where(account.c.id == id_account))
    accounts = [{"id_client": row.id_client, "id": row.id, 'balance': row.balance} for row in result]
    if accounts:
        return accounts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

@cnta.get("/get_total_usd/{id_account}" )
def get_total_usd(id_account: str):

    result = conn.execute(account.select().where(account.c.id == id_account)).fetchall()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    balance = result[0][2] if result and result[0][2] is not None else 0

    url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
    response = requests.get(url)
    if response.status_code == 200:
        data_dolar = response.json()
        balance_dolar = {'balance_pesos' : balance}
        monedas_a_calcular = ['Dolar Oficial', 'Dolar Blue', 'Dolar Soja', 'Dolar Contado con Liqui', 'Dolar Bolsa']
        for data in data_dolar:
            casa = data['casa']
            name = casa.get('nombre', '')
            if name in monedas_a_calcular and 'compra' in casa and casa['compra'] != 'No Cotiza':
                compra = float(casa['compra'].replace(",", "."))
                name = name.replace(" ", "_")
                balance_dolar[name] = round(balance / compra, 2)
        return [balance_dolar]
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Request error. Status code: {response.status_code}")

@cnta.post("/", response_model=Account)
def create_account(data: Account):
    new = {"id_client": data.id_client}
    print(data.id_client)
    client_exists = conn.execute(client.select().where(client.c.id == data.id_client)).first()
    if not client_exists:
        raise HTTPException(status_code=404, detail="Client not found")
    result = conn.execute(account.insert().values(new))
    new_id = result.inserted_primary_key[0]
    new["id"] = new_id
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating account")
    return new

@cnta.delete("/{id_account}")
def delete_account(id_account: str):
    result = conn.execute(account.delete().where(account.c.id == id_account))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="client not found")
    return {"message": "Account removed"}
