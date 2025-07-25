from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.doc_sequences import DocSequence
from src.db.schemas.doc_sequences import DocSequenceCreate
from typing import Optional

async def get_next_sequence(db: AsyncSession, doc_type: str, fiscal_year: str) -> int:
    result = await db.execute(
        select(DocSequence.last_sequence).where(
            DocSequence.doc_type == doc_type, DocSequence.fiscal_year == fiscal_year
        )
    )
    seq = result.scalar()
    if seq is None:
        db_seq = DocSequence(doc_type=doc_type, fiscal_year=fiscal_year, last_sequence=1)
        db.add(db_seq)
        await db.commit()
        return 1
    else:
        new_seq = seq + 1
        await db.execute(
            update(DocSequence).where(
                DocSequence.doc_type == doc_type, DocSequence.fiscal_year == fiscal_year
            ).values(last_sequence=new_seq)
        )
        await db.commit()
        return new_seq

async def increment_sequence(db: AsyncSession, doc_type: str, fiscal_year: str):
    stmt = update(DocSequence).where(
        DocSequence.doc_type == doc_type, DocSequence.fiscal_year == fiscal_year
    ).values(last_sequence=DocSequence.last_sequence + 1)
    await db.execute(stmt)
    await db.commit()