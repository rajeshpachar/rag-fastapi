from fastapi import (FastAPI, UploadFile,
                     HTTPException, Depends, BackgroundTasks)
import os
import shutil
import io
from app.db import get_db, File, FileChunk
from sqlalchemy.orm import Session
from app.libs.file_parser import FileParser
from app.tasks.background_tasks import TextProcessor, client
from sqlalchemy import select
from pydantic import BaseModel


app = FastAPI()




@app.get("/")
def root():
    return "Hello RAG fellow!"


