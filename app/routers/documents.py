import io
import os
import shutil
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile
from app.auth.auth_handler import get_user
from app.schemas import QuestionModel
from app.tasks.background_tasks import TextProcessor
from app.db import get_db, engine
from app.libs.file_parser import FileParser
from app.models import File
from sqlalchemy.orm import Session
from typing import List,Optional, Union


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/uploadfile/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile, db: Session = Depends(get_db), user: dict = Depends(get_user)): # noqa
    # Define allowed file extensions
    allowed_extensions = ["txt", "pdf"]

    file_content = await file.read()  # Read file content as bytes
    file_name = file.filename

    # # Check if the file extension is allowed
    file_extension = file.filename.split('.')[-1]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")

    folder = "sces"
    try:
        # Ensure the directory exists
        os.makedirs(folder, exist_ok=True)

        # Secure way to save the file
        file_location = os.path.join(folder, file.filename)

        file_content = await file.read()  # Read file content as bytes

        with open(file_location, "wb+") as file_object:
            # Convert bytes content to a file-like object
            file_like_object = io.BytesIO(file_content)
            # Use shutil.copyfileobj for secure file writing
            shutil.copyfileobj(file_like_object, file_object)

        content_parser = FileParser(file_location)
        file_text_content = content_parser.parse()
        # save file details in the database
        new_file = File(file_name=file.filename,
                        file_content=file_text_content,
                        file_type=file_extension)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        # Add background job for processing file content
        background_tasks.add_task(TextProcessor(db, new_file.id, 1024).chunk_and_embed, file_text_content) # noqa

        return {"info": "File saved", "filename": file.filename}

    except Exception as e:
        # Log the exception (add actual logging in production code)
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")

