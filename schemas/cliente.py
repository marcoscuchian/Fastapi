from typing import Optional
from pydantic import BaseModel

class Cliente(BaseModel):
    id_cliente: Optional[str] = None
    nombre: str