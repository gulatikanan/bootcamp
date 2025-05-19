from typing import List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from pydantic import BaseModel

Base = declarative_base()

# SQLAlchemy User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

# SQLAlchemy Post Model
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="posts")

# Pydantic Schemas
class PostSchema(BaseModel):
    id: Optional[int]
    title: str
    content: Optional[str]

    model_config = {
        "from_attributes": True
    }

class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    email: str
    posts: List[PostSchema] = []

    model_config = {
        "from_attributes": True
    }

# Database setup
engine = create_engine('sqlite:///users.db', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
