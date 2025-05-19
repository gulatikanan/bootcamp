# Schema-First vs Code-First Modeling

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import registry

engine = create_engine("sqlite:///:memory:")
metadata = MetaData()

# Simulate imported schema
user_table = Table("users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

metadata.create_all(engine)

# Reflect it into SQLAlchemy model
mapper_registry = registry()

class User:
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

mapper_registry.map_imperatively(User, user_table)

# Test insert and query
with engine.connect() as conn:
    conn.execute(user_table.insert(), {"id": 1, "name": "Kanan"})
    result = conn.execute(user_table.select())
    for row in result:
        print(row)

print("Schema-first model created and mapped.")