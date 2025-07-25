from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.sales_orders import SalesOrder
from src.db.models.sales_order_items import SalesOrderItem
from src.db.schemas.sales_orders import SalesOrderCreate, SalesOrderUpdate, SalesOrderInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_sales_order(db: AsyncSession, sales_order: SalesOrderCreate) -> SalesOrder:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "sales_order", fiscal_year)
    sales_order.sales_order_number = f"SO/{fiscal_year}/{seq:04d}"
    db_sales_order = SalesOrder(**sales_order.dict(exclude={'items'}))
    db.add(db_sales_order)
    await db.commit()
    await db.refresh(db_sales_order)
    for item in sales_order.items:
        db_item = SalesOrderItem(sales_order_id=db_sales_order.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "sales_order", fiscal_year)
    await db.refresh(db_sales_order)
    return db_sales_order

async def get_sales_orders(db: AsyncSession) -> List[SalesOrder]:
    result = await db.execute(select(SalesOrder))
    return result.scalars().all()

async def get_sales_order(db: AsyncSession, sales_order_id: int) -> Optional[SalesOrder]:
    result = await db.execute(select(SalesOrder).where(SalesOrder.id == sales_order_id))
    sales_order = result.scalar_one_or_none()
    if sales_order:
        result_items = await db.execute(select(SalesOrderItem).where(SalesOrderItem.sales_order_id == sales_order_id))
        sales_order.items = result_items.scalars().all()
    return sales_order

async def update_sales_order(db: AsyncSession, sales_order_id: int, sales_order_update: SalesOrderUpdate) -> Optional[SalesOrder]:
    stmt = update(SalesOrder).where(SalesOrder.id == sales_order_id).values(**sales_order_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if sales_order_update.items is not None:
        await db.execute(delete(SalesOrderItem).where(SalesOrderItem.sales_order_id == sales_order_id))
        for item in sales_order_update.items:
            db_item = SalesOrderItem(sales_order_id=sales_order_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_sales_order(db, sales_order_id)

async def delete_sales_order(db: AsyncSession, sales_order_id: int):
    await db.execute(delete(SalesOrderItem).where(SalesOrderItem.sales_order_id == sales_order_id))
    await db.execute(delete(SalesOrder).where(SalesOrder.id == sales_order_id))
    await db.commit()