from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.purchase_inv import create_purchase_inv, get_purchase_invs, get_purchase_inv, update_purchase_inv, delete_purchase_inv
from src.db.schemas.purchase_inv import PurchaseInvCreate, PurchaseInvInDB, PurchaseInvUpdate

router = APIRouter(tags=["purchase_invoices"])

@router.post("/", response_model=PurchaseInvInDB)
async def create_new_purchase_inv(purchase_inv: PurchaseInvCreate, db: AsyncSession = Depends(get_db)):
    return await create_purchase_inv(db, purchase_inv)

@router.get("/", response_model=List[PurchaseInvInDB])
async def read_purchase_invs(db: AsyncSession = Depends(get_db)):
    return await get_purchase_invs(db)

@router.get("/{purchase_inv_id}", response_model=PurchaseInvInDB)
async def read_purchase_inv(purchase_inv_id: int, db: AsyncSession = Depends(get_db)):
    db_purchase_inv = await get_purchase_inv(db, purchase_inv_id)
    if db_purchase_inv is None:
        raise HTTPException(status_code=404, detail="Purchase Invoice not found")
    return db_purchase_inv

@router.put("/{purchase_inv_id}", response_model=PurchaseInvInDB)
async def update_existing_purchase_inv(purchase_inv_id: int, purchase_inv: PurchaseInvUpdate, db: AsyncSession = Depends(get_db)):
    db_purchase_inv = await update_purchase_inv(db, purchase_inv_id, purchase_inv)
    if db_purchase_inv is None:
        raise HTTPException(status_code=404, detail="Purchase Invoice not found")
    return db_purchase_inv

@router.delete("/{purchase_inv_id}")
async def delete_existing_purchase_inv(purchase_inv_id: int, db: AsyncSession = Depends(get_db)):
    await delete_purchase_inv(db, purchase_inv_id)
    return {"detail": "Purchase Invoice deleted"}