

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
    prefix="/questions",
    tags=["Questions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/find-similar-chunks/{file_id}")
async def find_similar_chunks(file_id: int, question_data: QuestionModel,
                              db: Session = Depends(get_db), user: dict = Depends(get_user)):
    try:
        question = question_data.question

        vectors = [vector for idx, vector in build_googleai_embeddings(question)]
        question_embedding = vectors[0]
        # Create embeddings for the question
        # response = client.embeddings.create(input=question,
        #                                     model="text-embedding-ada-002")
        # question_embedding = response.data[0].embedding

        # Find similar chunks in the database
        similar_chunks_query = select(FileChunk).where(FileChunk.file_id == file_id)\
            .order_by(FileChunk.embedding_vector.l2_distance(question_embedding)).limit(10) # noqa
        similar_chunks = db.scalars(similar_chunks_query).all()

        # Format the response
        formatted_response = [
            {"chunk_id": chunk.chunk_id, "chunk_text": chunk.chunk_text}
            for chunk in similar_chunks
        ]

        return formatted_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
