from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.sales_orders import create_sales_order, get_sales_orders, get_sales_order, update_sales_order, delete_sales_order
from src.db.schemas.sales_orders import SalesOrderCreate, SalesOrderInDB, SalesOrderUpdate

router = APIRouter(tags=["sales_orders"])

@router.post("/", response_model=SalesOrderInDB)
async def create_new_sales_order(sales_order: SalesOrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_sales_order(db, sales_order)

@router.get("/", response_model=List[SalesOrderInDB])
async def read_sales_orders(db: AsyncSession = Depends(get_db)):
    return await get_sales_orders(db)

@router.get("/{sales_order_id}", response_model=SalesOrderInDB)
async def read_sales_order(sales_order_id: int, db: AsyncSession = Depends(get_db)):
    db_sales_order = await get_sales_order(db, sales_order_id)
    if db_sales_order is None:
        raise HTTPException(status_code=404, detail="Sales Order not found")
    return db_sales_order

@router.put("/{sales_order_id}", response_model=SalesOrderInDB)
async def update_existing_sales_order(sales_order_id: int, sales_order: SalesOrderUpdate, db: AsyncSession = Depends(get_db)):
    db_sales_order = await update_sales_order(db, sales_order_id, sales_order)
    if db_sales_order is None:
        raise HTTPException(status_code=404, detail="Sales Order not found")
    return db_sales_order

@router.delete("/{sales_order_id}")
async def delete_existing_sales_order(sales_order_id: int, db: AsyncSession = Depends(get_db)):
    await delete_sales_order(db, sales_order_id)
    return {"detail": "Sales Order deleted"}