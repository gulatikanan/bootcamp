from models import SessionLocal, User, Post

def add_post_for_user(email: str, title: str, content: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            print(f"❌ No user found with email '{email}'")
            return

        new_post = Post(title=title, content=content, user=user)
        session.add(new_post)
        session.commit()
        print(f"✅ Post added for user '{user.name}'")
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    add_post_for_user(
        email="alice@example.com", 
        title="My First Post", 
        content="This is Alice's first post!"
    )
