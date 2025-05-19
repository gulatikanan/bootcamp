from models import User, SessionLocal

def update_user_email(old_email: str, new_email: str) -> str:
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=old_email).first()
        if not user:
            return f"❌ User with email '{old_email}' not found."

        user.email = new_email
        session.commit()
        return f"✅ Email updated successfully to '{new_email}'."
    except Exception as e:
        session.rollback()
        return f"❌ Error updating user: {e}"
    finally:
        session.close()

if __name__ == "__main__":
    old_email = "alice@example.com"
    new_email = "alice.updated@example.com"
    message = update_user_email(old_email, new_email)
    print(message)
