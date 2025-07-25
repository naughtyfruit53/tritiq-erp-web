from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.grn import create_grn, get_grns, get_grn, update_grn, delete_grn
from src.db.schemas.grn import GrnCreate, GrnInDB, GrnUpdate

router = APIRouter(tags=["grn"])

@router.post("/", response_model=GrnInDB)
async def create_new_grn(grn: GrnCreate, db: AsyncSession = Depends(get_db)):
    return await create_grn(db, grn)

@router.get("/", response_model=List[GrnInDB])
async def read_grns(db: AsyncSession = Depends(get_db)):
    return await get_grns(db)

@router.get("/{grn_id}", response_model=GrnInDB)
async def read_grn(grn_id: int, db: AsyncSession = Depends(get_db)):
    db_grn = await get_grn(db, grn_id)
    if db_grn is None:
        raise HTTPException(status_code=404, detail="GRN not found")
    return db_grn

@router.put("/{grn_id}", response_model=GrnInDB)
async def update_existing_grn(grn_id: int, grn: GrnUpdate, db: AsyncSession = Depends(get_db)):
    db_grn = await update_grn(db, grn_id, grn)
    if db_grn is None:
        raise HTTPException(status_code=404, detail="GRN not found")
    return db_grn

@router.delete("/{grn_id}")
async def delete_existing_grn(grn_id: int, db: AsyncSession = Depends(get_db)):
    await delete_grn(db, grn_id)
    return {"detail": "GRN deleted"}