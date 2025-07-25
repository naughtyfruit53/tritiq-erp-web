from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.delivery_challans import DeliveryChallan
from src.db.models.delivery_challan_items import DeliveryChallanItem
from src.db.schemas.delivery_challans import DeliveryChallanCreate, DeliveryChallanUpdate, DeliveryChallanInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_delivery_challan(db: AsyncSession, delivery_challan: DeliveryChallanCreate) -> DeliveryChallan:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "delivery_challan", fiscal_year)
    delivery_challan.dc_number = f"DC/{fiscal_year}/{seq:04d}"
    db_delivery_challan = DeliveryChallan(**delivery_challan.dict(exclude={'items'}))
    db.add(db_delivery_challan)
    await db.commit()
    await db.refresh(db_delivery_challan)
    for item in delivery_challan.items:
        db_item = DeliveryChallanItem(dc_id=db_delivery_challan.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "delivery_challan", fiscal_year)
    await db.refresh(db_delivery_challan)
    return db_delivery_challan

async def get_delivery_challans(db: AsyncSession) -> List[DeliveryChallan]:
    result = await db.execute(select(DeliveryChallan))
    return result.scalars().all()

async def get_delivery_challan(db: AsyncSession, delivery_challan_id: int) -> Optional[DeliveryChallan]:
    result = await db.execute(select(DeliveryChallan).where(DeliveryChallan.id == delivery_challan_id))
    delivery_challan = result.scalar_one_or_none()
    if delivery_challan:
        result_items = await db.execute(select(DeliveryChallanItem).where(DeliveryChallanItem.dc_id == delivery_challan_id))
        delivery_challan.items = result_items.scalars().all()
    return delivery_challan

async def update_delivery_challan(db: AsyncSession, delivery_challan_id: int, delivery_challan_update: DeliveryChallanUpdate) -> Optional[DeliveryChallan]:
    stmt = update(DeliveryChallan).where(DeliveryChallan.id == delivery_challan_id).values(**delivery_challan_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if delivery_challan_update.items is not None:
        await db.execute(delete(DeliveryChallanItem).where(DeliveryChallanItem.dc_id == delivery_challan_id))
        for item in delivery_challan_update.items:
            db_item = DeliveryChallanItem(dc_id=delivery_challan_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_delivery_challan(db, delivery_challan_id)

async def delete_delivery_challan(db: AsyncSession, delivery_challan_id: int):
    await db.execute(delete(DeliveryChallanItem).where(DeliveryChallanItem.dc_id == delivery_challan_id))
    await db.execute(delete(DeliveryChallan).where(DeliveryChallan.id == delivery_challan_id))
    await db.commit()