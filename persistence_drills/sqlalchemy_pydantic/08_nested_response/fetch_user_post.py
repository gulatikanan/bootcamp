from models import SessionLocal, User, UserWithPostsSchema

def fetch_user_with_posts(email: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            print(f"❌ No user found with email '{email}'.")
            return

        user_schema = UserWithPostsSchema.model_validate(user)
        print("✅ User and posts fetched successfully!")
        print(user_schema.model_dump())  # Structured JSON-like dictionary
    finally:
        session.close()

if __name__ == "__main__":
    fetch_user_with_posts("alice@example.com")
