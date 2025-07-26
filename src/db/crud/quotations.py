# src/db/crud/quotations.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.quotations import Quote  # Changed from Quotation to Quote
from src.db.models.quotation_form import QuoteItem  # Assume QuoteItem for items
from src.db.schemas.quotations import QuoteCreate, QuoteUpdate, QuoteInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_quotation(db: AsyncSession, quotation: QuoteCreate) -> Quote:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "quotation", fiscal_year)
    quotation.quotation_number = f"QT/{fiscal_year}/{seq:04d}"
    db_quotation = Quote(**quotation.dict(exclude={'items'}))
    db.add(db_quotation)
    await db.commit()
    await db.refresh(db_quotation)
    for item in quotation.items:
        db_item = QuoteItem(quotation_id=db_quotation.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "quotation", fiscal_year)
    await db.refresh(db_quotation)
    return db_quotation

async def get_quotations(db: AsyncSession) -> List[Quote]:
    result = await db.execute(select(Quote))
    return result.scalars().all()

async def get_quotation(db: AsyncSession, quotation_id: int) -> Optional[Quote]:
    result = await db.execute(select(Quote).where(Quote.id == quotation_id))
    quotation = result.scalar_one_or_none()
    if quotation:
        result_items = await db.execute(select(QuoteItem).where(QuoteItem.quotation_id == quotation_id))
        quotation.items = result_items.scalars().all()
    return quotation

async def update_quotation(db: AsyncSession, quotation_id: int, quotation_update: QuoteUpdate) -> Optional[Quote]:
    stmt = update(Quote).where(Quote.id == quotation_id).values(**quotation_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if quotation_update.items is not None:
        await db.execute(delete(QuoteItem).where(QuoteItem.quotation_id == quotation_id))
        for item in quotation_update.items:
            db_item = QuoteItem(quotation_id=quotation_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_quotation(db, quotation_id)

async def delete_quotation(db: AsyncSession, quotation_id: int):
    await db.execute(delete(QuoteItem).where(QuoteItem.quotation_id == quotation_id))
    await db.execute(delete(Quote).where(Quote.id == quotation_id))
    await db.commit()