import io
import os
import shutil
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile
from sqlalchemy import desc, select
from app.auth.auth_handler import get_user
from app.schemas import QuestionModel
from app.tasks.background_tasks import TextProcessor
from app.db import get_db, engine
from app.libs.file_parser import FileParser
from app.models import File, FileChunk
from sqlalchemy.orm import Session
from typing import List,Optional, Union
from app.libs.constants import CHUNK_SIZE,CHUNK_OVERLAP
from app.tasks.embed_gen import gai_embeddings


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/uploadfile/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile, db: Session = Depends(get_db), user: dict = Depends(get_user)): # noqa
    # Define allowed file extensions
    allowed_extensions = ["txt", "pdf"]
    # # Check if the file extension is allowed
    file_extension = file.filename.split('.')[-1]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Define the folder to save the file
    folder = "sces"
    try:
        # Ensure the directory exists
        os.makedirs(folder, exist_ok=True)

        # Secure way to save the file
        file_location = os.path.join(folder, file.filename)

        file_content = file.file.read()  # Read file content as bytes

        with open(file_location, "wb+") as file_object:
            # Convert bytes content to a file-like object
            file_like_object = io.BytesIO(file_content)
            # Use shutil.copyfileobj for secure file writing
            shutil.copyfileobj(file_like_object, file_object)

        content_parser = FileParser(file_location)
        file_text_content = content_parser.parse()
        # save file details in the database
        new_file = File(file_name=file.filename,
                        file_length=len(file_text_content),
                        chunk_size = CHUNK_SIZE,
                        file_type=file_extension)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        # Add background job for processing file content
        background_tasks.add_task(TextProcessor(db, new_file.id, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP).chunk_and_embed, file_text_content) # noqa

        return {"info": "File saved", "filename": file.filename}

    except Exception as e:
        # Log the exception (add actual logging in production code)
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")


@router.post("/find-similar-chunks/{file_id}")
async def find_similar_chunks(file_id: int, question_data: QuestionModel,
                              db: Session = Depends(get_db), user: dict = Depends(get_user)):
    try:
        question = question_data.question
        question_embedding = gai_embeddings.embed_query(question)
      
        # Find similar chunks in the database
        # session.scalars(select(Item).order_by(Item.embedding.l2_distance([3, 1, 2])).limit(5))
#   Also supports max_inner_product and cosine_distance

        print(select(FileChunk))

        similar_chunks_query = select(FileChunk.id, FileChunk.chunk_index, FileChunk.chunk_text, FileChunk.vector.l2_distance(question_embedding).label("score")).where(FileChunk.file_id == file_id)\
            .order_by(desc(FileChunk.vector.l2_distance(question_embedding))).limit(10) # noqa
        print("#"*23)
        print(similar_chunks_query)
        print("#"*23)
        similar_chunks = db.scalars(similar_chunks_query).all()
        print(similar_chunks)
        print("#"*23)
        # Format the response
        formatted_response = [
            {"chunk_id": chunk.id, "chunk_text": chunk.chunk_text, "score": chunk.score}
            for chunk in similar_chunks
        ]

        return formatted_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
