from typing import Optional
from pydantic import BaseModel

class Clients(BaseModel):
    id: Optional[str] = None
    name: str