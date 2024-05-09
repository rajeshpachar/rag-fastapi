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



https://medium.com/@ashkangoleh/efficient-postgresql-connection-management-with-singleton-pattern-and-async-sync-engines-in-71b349e4c61d

https://www.reddit.com/r/FastAPI/comments/rfz8c1/a_neat_trick_for_async_database_session/

https://medium.com/datauniverse/optimizing-database-interaction-in-web-applications-connection-pooling-with-psycopg2-and-c56b37d155f8

testing

https://github.com/docugami/KG-RAG-datasets/tree/main/sec-10-q/data/v1/docs