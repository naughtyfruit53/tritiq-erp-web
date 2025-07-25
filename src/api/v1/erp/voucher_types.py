# src/api/v1/erp/voucher_types.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.voucher_types import create_voucher_type, get_voucher_types, get_voucher_type, update_voucher_type, delete_voucher_type
from src.db.schemas.voucher_types import VoucherTypeCreate, VoucherTypeInDB, VoucherTypeUpdate

router = APIRouter()

@router.post("/", response_model=VoucherTypeInDB)
async def create_new_voucher_type(voucher_type: VoucherTypeCreate, db: AsyncSession = Depends(get_db)):
    return await create_voucher_type(db, voucher_type)

@router.get("/", response_model=List[VoucherTypeInDB])
async def read_voucher_types(db: AsyncSession = Depends(get_db)):
    return await get_voucher_types(db)

@router.get("/{voucher_type_id}", response_model=VoucherTypeInDB)
async def read_voucher_type(voucher_type_id: int, db: AsyncSession = Depends(get_db)):
    db_voucher_type = await get_voucher_type(db, voucher_type_id)
    if db_voucher_type is None:
        raise HTTPException(status_code=404, detail="Voucher type not found")
    return db_voucher_type

@router.put("/{voucher_type_id}", response_model=VoucherTypeInDB)
async def update_existing_voucher_type(voucher_type_id: int, voucher_type: VoucherTypeUpdate, db: AsyncSession = Depends(get_db)):
    db_voucher_type = await update_voucher_type(db, voucher_type_id, voucher_type)
    if db_voucher_type is None:
        raise HTTPException(status_code=404, detail="Voucher type not found")
    return db_voucher_type

@router.delete("/{voucher_type_id}")
async def delete_existing_voucher_type(voucher_type_id: int, db: AsyncSession = Depends(get_db)):
    await delete_voucher_type(db, voucher_type_id)
    return {"detail": "Voucher type deleted"}