# app/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: Optional[str] = None
    description: Optional[str] = None

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None