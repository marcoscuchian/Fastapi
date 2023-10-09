from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class Movimiento(BaseModel):
    id_movimiento: Optional[str] = None
    id_cuenta: UUID
    tipo: str
    importe: float
    fecha: Optional[datetime] = None