# src/api/v1/erp/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db, AsyncSessionLocal
from src.db.crud.users import create_user, get_users, get_user, update_user, delete_user
from src.db.schemas.users import UserCreate, UserInDB, UserUpdate

router = APIRouter()

@router.post("/", response_model=UserInDB)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/", response_model=List[UserInDB])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@router.get("/{user_id}", response_model=UserInDB)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserInDB)
async def update_existing_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_user(db, user_id)
    return {"detail": "User deleted"}