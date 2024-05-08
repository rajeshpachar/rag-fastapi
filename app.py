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



@app.post("/find-similar-chunks/{file_id}")
async def find_similar_chunks(file_id: int, question_data: QuestionModel,
                              db: Session = Depends(get_db)):
    try:
        question = question_data.question

        # Create embeddings for the question
        response = client.embeddings.create(input=question,
                                            model="text-embedding-ada-002")
        question_embedding = response.data[0].embedding

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
