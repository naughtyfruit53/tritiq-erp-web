from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from ....db.models.doc_sequences import DocSequence  # Assume model exists: id, name, current_value
from typing import Optional

async def get_next_sequence_value(
    db: AsyncSession,
    sequence_name: str
) -> int:
    # Lock for update to handle concurrency
    result = await db.execute(
        select(DocSequence)
        .where(DocSequence.name == sequence_name)
        .with_for_update()
    )
    seq = result.scalar_one_or_none()
    
    if not seq:
        # Create new sequence
        stmt = insert(DocSequence).values(name=sequence_name, current_value=1)
        await db.execute(stmt)
        await db.commit()
        return 1
    
    # Update
    new_value = seq.current_value + 1
    seq.current_value = new_value
    await db.commit()
    return new_value

async def get_next_voucher_number(db: AsyncSession, voucher_type_id: int) -> str:
    fiscal_year = datetime.now().strftime("%y%y")
    sequence_name = f"voucher_{voucher_type_id}_{fiscal_year}"
    next_num = await get_next_sequence_value(db, sequence_name)
    return f"{sequence_name}/{next_num:04d}"  # Adjust format as needed