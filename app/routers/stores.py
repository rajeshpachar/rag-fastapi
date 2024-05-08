from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth_bearer import JWTBearer

from app.dependencies import get_token_header

from app.db import get_db
import app.schemas as schemas
from app.repositories import StoreRepo
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List,Optional


router = APIRouter(
    prefix="/stores",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post('/', tags=["Store"],response_model=schemas.Store,status_code=201, dependencies=[Depends(JWTBearer())])
async def create_store(store_request: schemas.StoreCreate, db: Session = Depends(get_db)):
    """
    Create a Store and save it in the database
    """
    db_store = StoreRepo.fetch_by_name(db, name=store_request.name)
    print(db_store)
    if db_store:
        raise HTTPException(status_code=400, detail="Store already exists!")

    return await StoreRepo.create(db=db, store=store_request)

@router.get('/', tags=["Store"],response_model=List[schemas.Store], dependencies=[Depends(JWTBearer())])
def get_all_stores(name: Optional[str] = None,db: Session = Depends(get_db)):
    """
    Get all the Stores stored in database
    """
    if name:
        stores =[]
        db_store = StoreRepo.fetch_by_name(db,name)
        print(db_store)
        stores.append(db_store)
        return stores
    else:
        return StoreRepo.fetch_all(db)
    
@router.get('/{store_id}', tags=["Store"],response_model=schemas.Store, dependencies=[Depends(JWTBearer())])
def get_store(store_id: int,db: Session = Depends(get_db)):
    """
    Get the Store with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db,store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found with the given ID")
    return db_store

@router.delete('/{store_id}', tags=["Store"], dependencies=[Depends(JWTBearer())])
async def delete_store(store_id: int,db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db,store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found with the given ID")
    await StoreRepo.delete(db,store_id)
    return "Store deleted successfully!"
    
