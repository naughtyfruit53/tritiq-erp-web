# src/api/v1/erp/voucher_columns.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.voucher_columns import create_voucher_column, get_voucher_columns, get_voucher_column, update_voucher_column, delete_voucher_column
from src.db.schemas.voucher_columns import VoucherColumnCreate, VoucherColumnInDB, VoucherColumnUpdate

router = APIRouter()

@router.post("/", response_model=VoucherColumnInDB)
async def create_new_voucher_column(voucher_column: VoucherColumnCreate, db: AsyncSession = Depends(get_db)):
    return await create_voucher_column(db, voucher_column)

@router.get("/{voucher_type_id}", response_model=List[VoucherColumnInDB])
async def read_voucher_columns(voucher_type_id: int, db: AsyncSession = Depends(get_db)):
    return await get_voucher_columns(db, voucher_type_id)

@router.get("/column/{voucher_column_id}", response_model=VoucherColumnInDB)
async def read_voucher_column(voucher_column_id: int, db: AsyncSession = Depends(get_db)):
    db_voucher_column = await get_voucher_column(db, voucher_column_id)
    if db_voucher_column is None:
        raise HTTPException(status_code=404, detail="Voucher column not found")
    return db_voucher_column

@router.put("/{voucher_column_id}", response_model=VoucherColumnInDB)
async def update_existing_voucher_column(voucher_column_id: int, voucher_column: VoucherColumnUpdate, db: AsyncSession = Depends(get_db)):
    db_voucher_column = await update_voucher_column(db, voucher_column_id, voucher_column)
    if db_voucher_column is None:
        raise HTTPException(status_code=404, detail="Voucher column not found")
    return db_voucher_column

@router.delete("/{voucher_column_id}")
async def delete_existing_voucher_column(voucher_column_id: int, db: AsyncSession = Depends(get_db)):
    await delete_voucher_column(db, voucher_column_id)
    return {"detail": "Voucher column deleted"}