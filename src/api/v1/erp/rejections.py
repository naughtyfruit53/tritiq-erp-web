from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.rejections import create_rejection, get_rejections, get_rejection, update_rejection, delete_rejection
from src.db.schemas.rejections import RejectionCreate, RejectionInDB, RejectionUpdate

router = APIRouter(tags=["rejections"])

@router.post("/", response_model=RejectionInDB)
async def create_new_rejection(rejection: RejectionCreate, db: AsyncSession = Depends(get_db)):
    return await create_rejection(db, rejection)

@router.get("/", response_model=List[RejectionInDB])
async def read_rejections(db: AsyncSession = Depends(get_db)):
    return await get_rejections(db)

@router.get("/{rejection_id}", response_model=RejectionInDB)
async def read_rejection(rejection_id: int, db: AsyncSession = Depends(get_db)):
    db_rejection = await get_rejection(db, rejection_id)
    if db_rejection is None:
        raise HTTPException(status_code=404, detail="Rejection not found")
    return db_rejection

@router.put("/{rejection_id}", response_model=RejectionInDB)
async def update_existing_rejection(rejection_id: int, rejection: RejectionUpdate, db: AsyncSession = Depends(get_db)):
    db_rejection = await update_rejection(db, rejection_id, rejection)
    if db_rejection is None:
        raise HTTPException(status_code=404, detail="Rejection not found")
    return db_rejection

@router.delete("/{rejection_id}")
async def delete_existing_rejection(rejection_id: int, db: AsyncSession = Depends(get_db)):
    await delete_rejection(db, rejection_id)
    return {"detail": "Rejection deleted"}