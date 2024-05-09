from sqlalchemy import Boolean, Column, Float, ForeignKey, Index, Integer, String, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, Text, ForeignKey
from pgvector.sqlalchemy import Vector

from app.db import Base

class BaseEntity(Base):
    __abstract__ = True
    id = Column(BigInteger, primary_key=True, index=True)
    create_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    created_by = Column(String(64))
    updated_by = Column(String(64))
    account_id = Column(String(64))
    account_name = Column(String(64))

schema_name = "rag"

class File(BaseEntity):
    __tablename__ = 'files'
    __table_args__ = {"schema": schema_name}

    file_name = Column(String(255))
    bucket_name = Column(String(255))
    bucket_key = Column(Text)
    file_length = Column(BigInteger)
    file_type = Column(String(16))
    chunk_size = Column(Integer)
    # file_hash = Column(String(255), unique=True)


class FileChunk(BaseEntity):
    __tablename__ = 'file_chunks'
    __table_args__ = {"schema": schema_name}
    # 
    file_id = Column(BigInteger,  ForeignKey(schema_name+'.files.id'))
    chunk_text = Column(Text)
    # conn.execute('CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops)')
    # https://github.com/pgvector/pgvector-python/blob/master/examples/bulk_loading.py
    vector = Column(Vector(768))
    chunk_index = Column(Integer)

class Questions(BaseEntity):
    __tablename__ = 'questions'
    __table_args__ = {"schema": schema_name}
    text = Column(Text)
    disabled = Column(Boolean)
    vector = Column(Vector(768))
    model  = Column(String(32))

class QuestionToDocuments(BaseEntity):
    __tablename__ = 'question_to_documents'
    __table_args__ = {"schema": schema_name}
    chunk_id = Column(BigInteger,  ForeignKey(schema_name+'.file_chunks.id'))
    ques_id = Column(BigInteger,  ForeignKey(schema_name+'.questions.id'))
    score = Column(Integer)

class QuestionAnswers(BaseEntity):
    __tablename__ = 'question_answers'
    __table_args__ = {"schema": schema_name}
    text = Column(Text)
    disabled = Column(Boolean)
    model  = Column(String(32))
    ques_id = Column(BigInteger,  ForeignKey(schema_name+'.questions.id'))

class AnswerFeedback(BaseEntity):
    __tablename__ = 'answer_feedback'
    __table_args__ = {"schema": schema_name}
    text = Column(Text)
    like = Column(Boolean)
    ans_id = Column(BigInteger,  ForeignKey(schema_name+'.questions.id'))


###################################
####### testing models
###############
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
