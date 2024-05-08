from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth_bearer import JWTBearer

from app.auth.auth_handler import get_user
# from app.dependencies import get_token_header

from app.db import get_db, engine
import app.schemas as schemas
from app.repositories import ItemRepo
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List,Optional, Union


router = APIRouter(
    prefix="/items",
    tags=["Items"],
    # dependencies=[Depends(get_user)],
    responses={404: {"description": "Not found"}},
)


# fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


# @router.get("/")
# async def read_items():
#     return fake_items_db


# @router.get("/{item_id}")
# async def read_item(item_id: str, ):
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}

# , dependencies=[Depends(JWTBearer())]
@router.post('/', tags=["Items"],response_model=schemas.Item,status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db), user: dict = Depends(get_user)):
    """
    Create an Item and store it in the database
    """
    
    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await ItemRepo.create(db=db, item=item_request)

@router.get('/', tags=["Items"],response_model= Union[List[schemas.Item], None])
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db), user: dict = Depends(get_user)):
    """
    Get all the Items stored in database
    """
    if name:
        items =[]
        db_item = ItemRepo.fetch_by_name(db,name)
        if db_item is not None:
            items.append(db_item)
        return items
    else:
        return ItemRepo.fetch_all(db)


@router.get('/{item_id}', tags=["Items"],response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db,item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item

@router.delete('/{item_id}', tags=["Items"])
async def delete_item(item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db,item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db,item_id)
    return "Item deleted successfully!"

@router.put('/{item_id}', tags=["Items"],response_model=schemas.Item)
async def update_item(item_id: int,item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.price = update_item_encoded['price']
        db_item.description = update_item_encoded['description']
        db_item.store_id = update_item_encoded['store_id']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
    
