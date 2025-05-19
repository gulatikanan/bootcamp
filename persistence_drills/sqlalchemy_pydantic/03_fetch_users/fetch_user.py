from models import User, UserSchema, SessionLocal, init_db

init_db()

def get_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        # Use model_validate for Pydantic v2
        return [UserSchema.model_validate(user) for user in users]
    finally:
        session.close()

if __name__ == "__main__":
    users = get_users()
    print(users)
