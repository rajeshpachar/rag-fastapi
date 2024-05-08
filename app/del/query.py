import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print(sa.__version__)  # 1.3.20
connection_uri = "mssql+pyodbc://@mssqlLocal64"
engine = sa.create_engine(connection_uri, echo=False)

# show existing sample data
with engine.connect() as conn:
    results = conn.execute(sa.text("SELECT * FROM users"))
    print([dict(r) for r in results])
    # [{'id': 1, 'name': 'Gord'}]
    results = conn.execute(sa.text("SELECT * FROM posts"))
    print([dict(r) for r in results])
    # [{'id': 1, 'user_id': 1, 'post': 'Hello world!'}]

Base = declarative_base()
meta = Base.metadata


class User(Base):
    __table__ = sa.Table("users", meta, autoload_with=engine)


class Post(Base):
    __table__ = sa.Table("posts", meta, autoload_with=engine)
    author = sa.orm.relationship("User")

    def __repr__(self):
        return f"<Post(id={self.id}, author_name='{self.author.name}', post='{self.post}')>"


Session = sessionmaker(bind=engine)
session = Session()

my_post = session.query(Post).get(1)
print(my_post)  # <Post(id=1, author_name='Gord', post='Hello world!')>
