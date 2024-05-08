from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, Text, ForeignKey
from pgvector.sqlalchemy import Vector

from .db import Base

class BaseEntity(Base):
    __abstract__ = True
    id = Column(BigInteger, primary_key=True, index=True)
    create_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    created_by = Column(String(64))
    updated_by = Column(String(64))
    account_id = Column(String(64))
    account_name = Column(String(64))

class File(BaseEntity):
    __tablename__ = 'files'
    file_name = Column(String(255))
    file_content = Column(Text)
    bucket_name = Column(String(255))
    bucket_key = Column(Text)
    


class FileChunk(BaseEntity):
    __tablename__ = 'file_chunks'
    file_id = Column(Integer,  ForeignKey('files.id'))
    chunk_text = Column(Text)
    embedding_vector = Column(Vector(1536))


class Item(BaseEntity):
    __tablename__ = "items"
    
    name = Column(String(80), nullable=False, unique=True,index=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200))
    store_id = Column(Integer,ForeignKey('stores.id'),nullable=False)
    def __repr__(self):
        return 'ItemModel(name=%s, price=%s,store_id=%s)' % (self.name, self.price,self.store_id)
    
class Store(BaseEntity):
    __tablename__ = "stores"
    name = Column(String(80), nullable=False, unique=True)
    items = relationship("Item",primaryjoin="Store.id == Item.store_id",cascade="all, delete-orphan")

    def __repr__(self):
        return 'Store(name=%s)' % self.name
