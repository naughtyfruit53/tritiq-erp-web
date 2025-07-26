# src/api/v1/erp/quotations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.quotations import create_quotation, get_quotations, get_quotation, update_quotation, delete_quotation
from src.db.schemas.quotations import QuoteCreate, QuoteInDB, QuoteUpdate

router = APIRouter(tags=["quotations"])

@router.post("/", response_model=QuoteInDB)
async def create_new_quotation(quotation: QuoteCreate, db: AsyncSession = Depends(get_db)):
    return await create_quotation(db, quotation)

@router.get("/", response_model=List[QuoteInDB])
async def read_quotations(db: AsyncSession = Depends(get_db)):
    return await get_quotations(db)

@router.get("/{quotation_id}", response_model=QuoteInDB)
async def read_quotation(quotation_id: int, db: AsyncSession = Depends(get_db)):
    db_quotation = await get_quotation(db, quotation_id)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return db_quotation

@router.put("/{quotation_id}", response_model=QuoteInDB)
async def update_existing_quotation(quotation_id: int, quotation: QuoteUpdate, db: AsyncSession = Depends(get_db)):
    db_quotation = await update_quotation(db, quotation_id, quotation)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return db_quotation

@router.delete("/{quotation_id}")
async def delete_existing_quotation(quotation_id: int, db: AsyncSession = Depends(get_db)):
    await delete_quotation(db, quotation_id)
    return {"detail": "Quotation deleted"}