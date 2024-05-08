from typing import List, Optional

from pydantic import BaseModel
import time

class BaseEntityModel(BaseModel):
    id: int
    # created_at: time
    # updated_at: time
    # created_by: str
    # updated_by: str
    # account_id: str
    # account_name: str

    # class Config:
    #     orm_mode = True

class ItemBase(BaseEntityModel):
    name: str
    price : float
    description: Optional[str] = None
    store_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    # class Config:
    #     orm_mode = True


class StoreBase(BaseEntityModel):
    name: str

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    items: List[Item] = []

    # class Config:
    #     orm_mode = True
