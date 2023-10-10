from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class Motion(BaseModel):
    id: Optional[str] = None
    id_account: str
    type: str
    amount: float
    date: Optional[datetime] = None