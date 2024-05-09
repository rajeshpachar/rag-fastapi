

import io
import os
import shutil
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile
from sqlalchemy import select
from app.auth.auth_handler import get_user
from app.schemas import QuestionModel
from app.tasks.background_tasks import TextProcessor
from app.db import get_db, engine
from app.libs.file_parser import FileParser
from app.models import File, FileChunk
from sqlalchemy.orm import Session
from typing import List,Optional, Union

from app.tasks.embed_gen import build_googleai_embeddings


router = APIRouter(
    prefix="/answers",
    tags=["Answers"],
    responses={404: {"description": "Not found"}},
)


