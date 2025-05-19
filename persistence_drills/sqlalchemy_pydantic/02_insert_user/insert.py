# from models import User, UserSchema, SessionLocal

# def insert_user(user_data: dict):
#     session = SessionLocal()
#     try:
#         # Validate input with Pydantic (id is optional now)
#         user = UserSchema(**user_data)

#         # Create SQLAlchemy user object (no id needed)
#         db_user = User(name=user.name, email=user.email)
#         session.add(db_user)
#         session.commit()
#         print("✅ User inserted successfully!")
#     except Exception as e:
#         session.rollback()
#         print(f"❌ Error inserting user: {e}")
#     finally:
#         session.close()

# if __name__ == "__main__":
#     new_user = {"name": "Alice", "email": "alice@example.com"}
#     insert_user(new_user)

from models import User, SessionLocal

def insert_sample_user():
    session = SessionLocal()
    try:
        user = User(name="Alice", email="alice@example.com")
        session.add(user)
        session.commit()
        print("User inserted.")
    except Exception as e:
        session.rollback()
        print("Error inserting user:", e)
    finally:
        session.close()

if __name__ == "__main__":
    insert_sample_user()
