# src/db/crud/credit_notes.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.credit_notes import CreditNote
from src.db.models.cn_items import CnItem
from src.db.schemas.credit_notes import CreditNoteCreate, CreditNoteUpdate, CreditNoteInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_credit_note(db: AsyncSession, credit_note: CreditNoteCreate) -> CreditNote:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "credit_note", fiscal_year)
    credit_note.cn_number = f"CN/{fiscal_year}/{seq:04d}"
    db_credit_note = CreditNote(**credit_note.dict(exclude={'items'}))
    db.add(db_credit_note)
    await db.commit()
    await db.refresh(db_credit_note)
    for item in credit_note.items:
        db_item = CnItem(cn_id=db_credit_note.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "credit_note", fiscal_year)
    await db.refresh(db_credit_note)
    return db_credit_note

async def get_credit_notes(db: AsyncSession) -> List[CreditNote]:
    result = await db.execute(select(CreditNote))
    return result.scalars().all()

async def get_credit_note(db: AsyncSession, credit_note_id: int) -> Optional[CreditNote]:
    result = await db.execute(select(CreditNote).where(CreditNote.id == credit_note_id))
    credit_note = result.scalar_one_or_none()
    if credit_note:
        result_items = await db.execute(select(CnItem).where(CnItem.cn_id == credit_note_id))
        credit_note.items = result_items.scalars().all()
    return credit_note

async def update_credit_note(db: AsyncSession, credit_note_id: int, credit_note_update: CreditNoteUpdate) -> Optional[CreditNote]:
    stmt = update(CreditNote).where(CreditNote.id == credit_note_id).values(**credit_note_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if credit_note_update.items is not None:
        await db.execute(delete(CnItem).where(CnItem.cn_id == credit_note_id))
        for item in credit_note_update.items:
            db_item = CnItem(cn_id=credit_note_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_credit_note(db, credit_note_id)

async def delete_credit_note(db: AsyncSession, credit_note_id: int):
    await db.execute(delete(CnItem).where(CnItem.cn_id == credit_note_id))
    await db.execute(delete(CreditNote).where(CreditNote.id == credit_note_id))
    await db.commit()