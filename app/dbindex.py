

from sqlalchemy import Index

from app.models import FileChunk
from app.db import engine

# https://github.com/pgvector/pgvector-python/blob/master/README.md
# index = Index(
#     'my_index',
#     FileChunk.embedding,
#     postgresql_using='hnsw',
#     postgresql_with={'m': 16, 'ef_construction': 64},
#     postgresql_ops={'embedding': 'vector_l2_ops'}
# )
# # or
# index = Index(
#     'my_index',
#     FileChunk.embedding,
#     postgresql_using='ivfflat',
#     postgresql_with={'lists': 100},
#     postgresql_ops={'embedding': 'vector_l2_ops'}
# )

# index.create(engine)