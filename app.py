from fastapi import FastAPI
from routes.cliente import clte
from routes.categoria import cat
from routes.movimientos import mvnto
from routes.cuenta import cnta
from routes.categoriacliente import catClien


app = FastAPI(
    title= "Banza Challenge",
    description= "Proceso de selección para trabajar en Banza.",
)

app.include_router(clte)
app.include_router(cnta)
app.include_router(cat)
app.include_router(catClien)
app.include_router(mvnto)
