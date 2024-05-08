#
# FROM python:3.9

#

# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# https://testdriven.io/blog/fastapi-docker-traefik/
# set env variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

#
# RUN pip install --no-cache-dir -r requirements.txt
#


#
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
