from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Account(BaseModel):
    id: Optional[str] = None
    id_client: str
    balance: float = 0