from models import User, SessionLocal

def bulk_insert_users(user_list):
    session = SessionLocal()
    try:
        # Convert each dict to a User instance
        users = [User(**data) for data in user_list]

        # Add all users at once
        session.add_all(users)

        # Commit the transaction
        session.commit()
        print(f"✅ {len(users)} users inserted successfully!")
    except Exception as e:
        session.rollback()
        print(f"❌ Error during bulk insert: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    users_to_add = [
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Carol", "email": "carol@example.com"},
        {"name": "Kanan", "email": "kanan@example.com"}  
    ]
    bulk_insert_users(users_to_add)
