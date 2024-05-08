from typing import List, Optional

from pydantic import BaseModel
import time


class QuestionModel(BaseModel):
    question: str


# class PageContent(BaseModel):
#     page_num: int
#     content: str

# class DocumentContent(BaseModel):
#     pages: List[PageContent] = []
#     document_length: int


###################################

class ItemBase(BaseModel):
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


class StoreBase(BaseModel):
    name: str

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    items: List[Item] = []

    # class Config:
    #     orm_mode = True
