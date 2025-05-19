from models import User, UserSchema, SessionLocal

def get_user_by_email(email: str) -> UserSchema | None:
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=email).first()  # ORM filtering
        if user:
            return UserSchema.model_validate(user)  # ORM to Pydantic (v2 syntax)
        else:
            return None
    finally:
        session.close()

if __name__ == "__main__":
    email = "alice@example.com"
    result = get_user_by_email(email)
    if result:
        print("✅ User found:", result)
    else:
        print("❌ No user found with that email.")
