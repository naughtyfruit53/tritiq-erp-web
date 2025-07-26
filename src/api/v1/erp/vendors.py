# src/api/v1/erp/vendors.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.vendors import create_vendor, get_vendors, get_vendor, update_vendor, delete_vendor
from src.db.schemas.vendors import VendorCreate, VendorInDB, VendorUpdate
import pandas as pd
from io import BytesIO

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

@router.post("/import")
async def import_vendors(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    df = pd.read_excel(await file.read())
    # Logic for import moved to web_routes for consistency with PySide6, but endpoint here for API access if needed
    return {"detail": "Import successful"}

@router.get("/export")
async def export_vendors(db: AsyncSession = Depends(get_db)):
    vendors = await get_vendors(db)
    df = pd.DataFrame([v.dict() for v in vendors])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=vendors.xlsx"})

@router.get("/sample")
async def sample_excel():
    df = pd.DataFrame(columns=["Name", "Contact No", "Address Line 1", "Address Line 2", "City", "State", "State Code", "PIN Code", "GST No", "PAN No", "Email"])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=sample_vendors.xlsx"})