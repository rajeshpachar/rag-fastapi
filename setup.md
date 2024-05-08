mkdir app && \
  touch app/__init__.py app/main.py requirements.txt

fastapi==0.89.1
uvicorn==0.20.0

local

uvicorn app.main:app --reload

or

https://testdriven.io/blog/fastapi-docker-traefik/

docker-compose build
docker-compose up -d
