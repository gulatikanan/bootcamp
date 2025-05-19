import asyncio
from database import AsyncSessionLocal
from models import User
from sqlalchemy import select

async def create_user(name: str, email: str):
    async with AsyncSessionLocal() as session:
        try:
            user = User(name=name, email=email)
            session.add(user)
            await session.commit()
            print("✅ User created:", user.name)
        except Exception as e:
            await session.rollback()
            print("❌ Error:", e)

async def get_user_by_email(email: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            print(f"✅ User found: {user.name}, Email: {user.email}")
        else:
            print("❌ No user found with that email")

if __name__ == "__main__":
    asyncio.run(create_user("Eve", "eve@example.com"))
    asyncio.run(get_user_by_email("eve@example.com"))
