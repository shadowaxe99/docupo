from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    filename = Column(String)
    format = Column(String)
    upload_time = Column(DateTime)

class Repository(Base):
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    document_id = Column(Integer)
    repo_name = Column(String)
    creation_time = Column(DateTime)
    last_push_time = Column(DateTime)
```