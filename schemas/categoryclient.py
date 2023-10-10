from typing import Optional
from uuid import UUID
from pydantic import BaseModel



class Categoryclient(BaseModel):
    id_category: str
    id_client: str
