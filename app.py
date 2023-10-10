from fastapi import FastAPI
from routes.client import clte
from routes.category import cat
from routes.motion import mvnto
from routes.account import cnta
from routes.categoryclient import catClien


app = FastAPI(
    title= "Banza Challenge",
    description= "Proceso de selección para trabajar en Banza.",
)

app.include_router(clte)
app.include_router(cnta)
app.include_router(cat)
app.include_router(catClien)
app.include_router(mvnto)
