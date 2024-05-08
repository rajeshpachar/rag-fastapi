# rag-fastapi
A simple implementation of RAG (Retrieval Augmented Generation) using fastapi and postgreSQL (with pgvector for vector embeddings).

python3 -m venv .venv
source ./.venv/bin/activate

Contributions are welcomed to make this a more comprehensive package.


https://fastapi.tiangolo.com/tutorial/bigger-applications/

https://scriptable.com/postgresql/how-to-install-pgvector-postgresql-mac-docker/#:~:text=You%20must%20launch%20the%20app,Step%203.

docker pull pgvector/pgvector:pg16 


docker volume create postgres-volume

docker run --name pgvector-container -e POSTGRES_PASSWORD=docker_user -e POSTGRES_USER=docker_user -p 5433:5432 -v postgres-volume:/var/lib/postgresql/data -d pgvector/pgvector:pg16 



##### docker run --name pgvector-container -e POSTGRES_PASSWORD=mysecretpassword -p 5433:5432 -d postgres

docker exec -it pgvector-container bash
docker exec -it pgvector-container psql -U docker_user



psql -U docker_user

CREATE ROLE docker_user with login SUPERUSER PASSWORD ‘docker_user’;
ALTER USER docker_user WITH CREATEDB CREATEROLE;


CREATE DATABASE dbtest;


CREATE TABLE accounts (
account_id serial PRIMARY KEY,
name VARCHAR (50) NOT NULL);
INSERT INTO accounts (account_id, name)
VALUES (1, 'HBL');
SELECT * from accounts;


######

\d: Display all tables, indexes, views, and sequences.
\dt: Display all tables.
\di: Display all indexes.
\dv: Display all views.
\ds: Display all sequences.
\dT: Display all types.
\dS: Display all system tables.
\du: Display all users.

https://www3.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html


https://fastapi.tiangolo.com/tutorial/sql-databases/