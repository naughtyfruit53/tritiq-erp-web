from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.grn import Grn
from src.db.models.grn_items import GrnItem
from src.db.schemas.grn import GrnCreate, GrnUpdate, GrnInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_grn(db: AsyncSession, grn: GrnCreate) -> Grn:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "grn", fiscal_year)
    grn.grn_number = f"GRN/{fiscal_year}/{seq:04d}"
    db_grn = Grn(**grn.dict(exclude={'items'}))
    db.add(db_grn)
    await db.commit()
    await db.refresh(db_grn)
    for item in grn.items:
        db_item = GrnItem(grn_id=db_grn.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "grn", fiscal_year)
    await db.refresh(db_grn)
    return db_grn

async def get_grns(db: AsyncSession) -> List[Grn]:
    result = await db.execute(select(Grn))
    return result.scalars().all()

async def get_grn(db: AsyncSession, grn_id: int) -> Optional[Grn]:
    result = await db.execute(select(Grn).where(Grn.id == grn_id))
    grn = result.scalar_one_or_none()
    if grn:
        result_items = await db.execute(select(GrnItem).where(GrnItem.grn_id == grn_id))
        grn.items = result_items.scalars().all()
    return grn

async def update_grn(db: AsyncSession, grn_id: int, grn_update: GrnUpdate) -> Optional[Grn]:
    stmt = update(Grn).where(Grn.id == grn_id).values(**grn_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if grn_update.items is not None:
        await db.execute(delete(GrnItem).where(GrnItem.grn_id == grn_id))
        for item in grn_update.items:
            db_item = GrnItem(grn_id=grn_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_grn(db, grn_id)

async def delete_grn(db: AsyncSession, grn_id: int):
    await db.execute(delete(GrnItem).where(GrnItem.grn_id == grn_id))
    await db.execute(delete(Grn).where(Grn.id == grn_id))
    await db.commit()