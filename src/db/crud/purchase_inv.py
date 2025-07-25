from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.purchase_inv import PurchaseInv
from src.db.models.purchase_inv_items import PurchaseInvItem
from src.db.schemas.purchase_inv import PurchaseInvCreate, PurchaseInvUpdate, PurchaseInvInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_purchase_inv(db: AsyncSession, purchase_inv: PurchaseInvCreate) -> PurchaseInv:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "purchase_inv", fiscal_year)
    purchase_inv.pur_inv_number = f"PUR_INV/{fiscal_year}/{seq:04d}"
    db_purchase_inv = PurchaseInv(**purchase_inv.dict(exclude={'items'}))
    db.add(db_purchase_inv)
    await db.commit()
    await db.refresh(db_purchase_inv)
    for item in purchase_inv.items:
        db_item = PurchaseInvItem(pur_inv_id=db_purchase_inv.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "purchase_inv", fiscal_year)
    await db.refresh(db_purchase_inv)
    return db_purchase_inv

async def get_purchase_invs(db: AsyncSession) -> List[PurchaseInv]:
    result = await db.execute(select(PurchaseInv))
    return result.scalars().all()

async def get_purchase_inv(db: AsyncSession, purchase_inv_id: int) -> Optional[PurchaseInv]:
    result = await db.execute(select(PurchaseInv).where(PurchaseInv.id == purchase_inv_id))
    purchase_inv = result.scalar_one_or_none()
    if purchase_inv:
        result_items = await db.execute(select(PurchaseInvItem).where(PurchaseInvItem.pur_inv_id == purchase_inv_id))
        purchase_inv.items = result_items.scalars().all()
    return purchase_inv

async def update_purchase_inv(db: AsyncSession, purchase_inv_id: int, purchase_inv_update: PurchaseInvUpdate) -> Optional[PurchaseInv]:
    stmt = update(PurchaseInv).where(PurchaseInv.id == purchase_inv_id).values(**purchase_inv_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if purchase_inv_update.items is not None:
        await db.execute(delete(PurchaseInvItem).where(PurchaseInvItem.pur_inv_id == purchase_inv_id))
        for item in purchase_inv_update.items:
            db_item = PurchaseInvItem(pur_inv_id=purchase_inv_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_purchase_inv(db, purchase_inv_id)

async def delete_purchase_inv(db: AsyncSession, purchase_inv_id: int):
    await db.execute(delete(PurchaseInvItem).where(PurchaseInvItem.pur_inv_id == purchase_inv_id))
    await db.execute(delete(PurchaseInv).where(PurchaseInv.id == purchase_inv_id))
    await db.commit()