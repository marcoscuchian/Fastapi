from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Cuenta(BaseModel):
    id_cuenta: Optional[str] = None
    id_cliente: UUID
    saldo: float = 0