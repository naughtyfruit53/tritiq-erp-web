from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.purchase_orders import PurchaseOrder
from src.db.models.po_items import PoItem
from src.db.schemas.purchase_orders import PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_purchase_order(db: AsyncSession, purchase_order: PurchaseOrderCreate) -> PurchaseOrder:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "purchase_order", fiscal_year)
    purchase_order.po_number = f"PO/{fiscal_year}/{seq:04d}"
    db_purchase_order = PurchaseOrder(**purchase_order.dict(exclude={'items'}))
    db.add(db_purchase_order)
    await db.commit()
    await db.refresh(db_purchase_order)
    for item in purchase_order.items:
        db_item = PoItem(po_id=db_purchase_order.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "purchase_order", fiscal_year)
    await db.refresh(db_purchase_order)
    return db_purchase_order

async def get_purchase_orders(db: AsyncSession) -> List[PurchaseOrder]:
    result = await db.execute(select(PurchaseOrder))
    return result.scalars().all()

async def get_purchase_order(db: AsyncSession, purchase_order_id: int) -> Optional[PurchaseOrder]:
    result = await db.execute(select(PurchaseOrder).where(PurchaseOrder.id == purchase_order_id))
    purchase_order = result.scalar_one_or_none()
    if purchase_order:
        result_items = await db.execute(select(PoItem).where(PoItem.po_id == purchase_order_id))
        purchase_order.items = result_items.scalars().all()
    return purchase_order

async def update_purchase_order(db: AsyncSession, purchase_order_id: int, purchase_order_update: PurchaseOrderUpdate) -> Optional[PurchaseOrder]:
    stmt = update(PurchaseOrder).where(PurchaseOrder.id == purchase_order_id).values(**purchase_order_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if purchase_order_update.items is not None:
        await db.execute(delete(PoItem).where(PoItem.po_id == purchase_order_id))
        for item in purchase_order_update.items:
            db_item = PoItem(po_id=purchase_order_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_purchase_order(db, purchase_order_id)

async def delete_purchase_order(db: AsyncSession, purchase_order_id: int):
    await db.execute(delete(PoItem).where(PoItem.po_id == purchase_order_id))
    await db.execute(delete(PurchaseOrder).where(PurchaseOrder.id == purchase_order_id))
    await db.commit()