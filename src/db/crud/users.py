# src/db/crud/users.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.users import User
from src.db.schemas.users import UserCreate, UserUpdate
from typing import List, Optional

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(username=user.username, password=user.password, role=user.role, active=user.active, must_change_password=user.must_change_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# New: For login
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    if user_update.password:  # Hash if updating password
        user_update.password = bcrypt.hashpw(user_update.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    stmt = update(User).where(User.id == user_id).values(**user_update.dict(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    return await get_user(db, user_id)

async def delete_user(db: AsyncSession, user_id: int):
    stmt = delete(User).where(User.id == user_id)
    await db.execute(stmt)
    await db.commit()