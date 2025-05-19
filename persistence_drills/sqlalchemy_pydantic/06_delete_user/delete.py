from models import User, SessionLocal

def delete_user_by_email(email: str) -> str:
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            return f"❌ User with email '{email}' not found."

        session.delete(user)
        session.commit()
        return f"🗑️ User with email '{email}' deleted successfully."
    except Exception as e:
        session.rollback()
        return f"❌ Error deleting user: {e}"
    finally:
        session.close()

if __name__ == "__main__":
    email_to_delete = "alice.updated@example.com"  # Use the email after your update
    result = delete_user_by_email(email_to_delete)
    print(result)
