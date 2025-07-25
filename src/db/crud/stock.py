from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.stock import Stock
from src.db.schemas.stock import StockCreate, StockUpdate, StockInDB
from typing import List, Optional

async def create_stock(db: AsyncSession, stock: StockCreate) -> Stock:
    db_stock = Stock(**stock.dict())
    db.add(db_stock)
    await db.commit()
    await db.refresh(db_stock)
    return db_stock

async def get_stocks(db: AsyncSession) -> List[Stock]:
    result = await db.execute(select(Stock))
    return result.scalars().all()

async def get_stock(db: AsyncSession, stock_id: int) -> Optional[Stock]:
    result = await db.execute(select(Stock).where(Stock.id == stock_id))
    return result.scalar_one_or_none()

async def update_stock(db: AsyncSession, stock_id: int, stock_update: StockUpdate) -> Optional[Stock]:
    stmt = update(Stock).where(Stock.id == stock_id).values(**stock_update.dict(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    return await get_stock(db, stock_id)

async def delete_stock(db: AsyncSession, stock_id: int):
    await db.execute(delete(Stock).where(Stock.id == stock_id))
    await db.commit()