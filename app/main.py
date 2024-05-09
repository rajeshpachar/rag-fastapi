
import os
from dotenv import load_dotenv,find_dotenv

from app.routers import stores
# Find the .env file
dotenv_path = find_dotenv()
output = load_dotenv(dotenv_path, override=True)

print("####"*10)
print(os.getenv('POSTGRES_USERNAME'))
print("####"*10)
# exit()

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

import time
from fastapi.middleware.gzip import GZipMiddleware

from app.routers import items,documents
from app.db import get_db, engine
import app.models as models


# Import the token validation function from the token_validation module


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()


# app.add_middleware(GZipMiddleware, minimum_size=1000)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)


# @app.exception_handler(Exception)
# def validation_exception_handler(request, err):
#     base_error_message = f"Failed to execute: {request.method}: {request.url}"
#     return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

app.include_router(documents.router)
app.include_router(items.router)
app.include_router(stores.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

