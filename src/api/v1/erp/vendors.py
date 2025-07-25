# src/api/v1/erp/vendors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.vendors import create_vendor, get_vendors, get_vendor, update_vendor, delete_vendor
from src.db.schemas.vendors import VendorCreate, VendorInDB, VendorUpdate

router = APIRouter()

@router.post("/", response_model=VendorInDB)
async def create_new_vendor(vendor: VendorCreate, db: AsyncSession = Depends(get_db)):
    return await create_vendor(db, vendor)

@router.get("/", response_model=List[VendorInDB])
async def read_vendors(db: AsyncSession = Depends(get_db)):
    return await get_vendors(db)

@router.get("/{vendor_id}", response_model=VendorInDB)
async def read_vendor(vendor_id: int, db: AsyncSession = Depends(get_db)):
    db_vendor = await get_vendor(db, vendor_id)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.put("/{vendor_id}", response_model=VendorInDB)
async def update_existing_vendor(vendor_id: int, vendor: VendorUpdate, db: AsyncSession = Depends(get_db)):
    db_vendor = await update_vendor(db, vendor_id, vendor)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.delete("/{vendor_id}")
async def delete_existing_vendor(vendor_id: int, db: AsyncSession = Depends(get_db)):
    await delete_vendor(db, vendor_id)
    return {"detail": "Vendor deleted"}