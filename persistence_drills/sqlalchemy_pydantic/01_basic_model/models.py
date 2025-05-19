from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import os

Base = declarative_base()

# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Pydantic Schema
class UserSchema(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "users.db")

engine = create_engine(f"sqlite:///{db_path}", echo=True)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
