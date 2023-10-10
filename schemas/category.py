from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: Optional[str] = None
    name: str
