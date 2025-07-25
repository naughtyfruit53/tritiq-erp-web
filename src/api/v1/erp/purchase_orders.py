from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.purchase_orders import create_purchase_order, get_purchase_orders, get_purchase_order, update_purchase_order, delete_purchase_order
from src.db.schemas.purchase_orders import PurchaseOrderCreate, PurchaseOrderInDB, PurchaseOrderUpdate

router = APIRouter(tags=["purchase_orders"])

@router.post("/", response_model=PurchaseOrderInDB)
async def create_new_purchase_order(purchase_order: PurchaseOrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_purchase_order(db, purchase_order)

@router.get("/", response_model=List[PurchaseOrderInDB])
async def read_purchase_orders(db: AsyncSession = Depends(get_db)):
    return await get_purchase_orders(db)

@router.get("/{purchase_order_id}", response_model=PurchaseOrderInDB)
async def read_purchase_order(purchase_order_id: int, db: AsyncSession = Depends(get_db)):
    db_purchase_order = await get_purchase_order(db, purchase_order_id)
    if db_purchase_order is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return db_purchase_order

@router.put("/{purchase_order_id}", response_model=PurchaseOrderInDB)
async def update_existing_purchase_order(purchase_order_id: int, purchase_order: PurchaseOrderUpdate, db: AsyncSession = Depends(get_db)):
    db_purchase_order = await update_purchase_order(db, purchase_order_id, purchase_order)
    if db_purchase_order is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return db_purchase_order

@router.delete("/{purchase_order_id}")
async def delete_existing_purchase_order(purchase_order_id: int, db: AsyncSession = Depends(get_db)):
    await delete_purchase_order(db, purchase_order_id)
    return {"detail": "Purchase Order deleted"}