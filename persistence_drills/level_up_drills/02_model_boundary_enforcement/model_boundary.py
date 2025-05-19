from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Define a Pydantic model for API response
class UserOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True  # Required in Pydantic v2 to enable ORM parsing
    }

# Setup
engine = create_engine("sqlite:///example.db", echo=False)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample user
session.add(User(name="anurag"))
session.commit()

# API Layer: safely convert ORM -> Pydantic model
def get_user_as_pydantic(user_id: int) -> UserOut:
    db_user = session.query(User).filter_by(id=user_id).first()
    if not db_user:
        raise ValueError("User not found")
    return UserOut.model_validate(db_user)

# Simulate controller printing user API response
print(get_user_as_pydantic(1))