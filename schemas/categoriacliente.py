from typing import Optional
from uuid import UUID
from pydantic import BaseModel



class CategoriaCliente(BaseModel):
    id_categoria: Optional[str] = None
    id_cliente: UUID
