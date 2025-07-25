from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.delivery_challans import create_delivery_challan, get_delivery_challans, get_delivery_challan, update_delivery_challan, delete_delivery_challan
from src.db.schemas.delivery_challans import DeliveryChallanCreate, DeliveryChallanInDB, DeliveryChallanUpdate

router = APIRouter(tags=["delivery_challans"])

@router.post("/", response_model=DeliveryChallanInDB)
async def create_new_delivery_challan(delivery_challan: DeliveryChallanCreate, db: AsyncSession = Depends(get_db)):
    return await create_delivery_challan(db, delivery_challan)

@router.get("/", response_model=List[DeliveryChallanInDB])
async def read_delivery_challans(db: AsyncSession = Depends(get_db)):
    return await get_delivery_challans(db)

@router.get("/{delivery_challan_id}", response_model=DeliveryChallanInDB)
async def read_delivery_challan(delivery_challan_id: int, db: AsyncSession = Depends(get_db)):
    db_delivery_challan = await get_delivery_challan(db, delivery_challan_id)
    if db_delivery_challan is None:
        raise HTTPException(status_code=404, detail="Delivery Challan not found")
    return db_delivery_challan

@router.put("/{delivery_challan_id}", response_model=DeliveryChallanInDB)
async def update_existing_delivery_challan(delivery_challan_id: int, delivery_challan: DeliveryChallanUpdate, db: AsyncSession = Depends(get_db)):
    db_delivery_challan = await update_delivery_challan(db, delivery_challan_id, delivery_challan)
    if db_delivery_challan is None:
        raise HTTPException(status_code=404, detail="Delivery Challan not found")
    return db_delivery_challan

@router.delete("/{delivery_challan_id}")
async def delete_existing_delivery_challan(delivery_challan_id: int, db: AsyncSession = Depends(get_db)):
    await delete_delivery_challan(db, delivery_challan_id)
    return {"detail": "Delivery Challan deleted"}