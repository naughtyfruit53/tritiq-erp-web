from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.stock import create_stock, get_stocks, get_stock, update_stock, delete_stock
from src.db.schemas.stock import StockCreate, StockInDB, StockUpdate

router = APIRouter(tags=["stock"])

@router.post("/", response_model=StockInDB)
async def create_new_stock(stock: StockCreate, db: AsyncSession = Depends(get_db)):
    return await create_stock(db, stock)

@router.get("/", response_model=List[StockInDB])
async def read_stocks(db: AsyncSession = Depends(get_db)):
    return await get_stocks(db)

@router.get("/{stock_id}", response_model=StockInDB)
async def read_stock(stock_id: int, db: AsyncSession = Depends(get_db)):
    db_stock = await get_stock(db, stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock

@router.put("/{stock_id}", response_model=StockInDB)
async def update_existing_stock(stock_id: int, stock: StockUpdate, db: AsyncSession = Depends(get_db)):
    db_stock = await update_stock(db, stock_id, stock)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock

@router.delete("/{stock_id}")
async def delete_existing_stock(stock_id: int, db: AsyncSession = Depends(get_db)):
    await delete_stock(db, stock_id)
    return {"detail": "Stock deleted"}