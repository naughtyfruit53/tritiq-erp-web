from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.rejections import Rejection
from src.db.schemas.rejections import RejectionCreate, RejectionUpdate, RejectionInDB
from typing import List, Optional

async def create_rejection(db: AsyncSession, rejection: RejectionCreate) -> Rejection:
    db_rejection = Rejection(**rejection.dict())
    db.add(db_rejection)
    await db.commit()
    await db.refresh(db_rejection)
    return db_rejection

async def get_rejections(db: AsyncSession) -> List[Rejection]:
    result = await db.execute(select(Rejection))
    return result.scalars().all()

async def get_rejection(db: AsyncSession, rejection_id: int) -> Optional[Rejection]:
    result = await db.execute(select(Rejection).where(Rejection.id == rejection_id))
    return result.scalar_one_or_none()

async def update_rejection(db: AsyncSession, rejection_id: int, rejection_update: RejectionUpdate) -> Optional[Rejection]:
    stmt = update(Rejection).where(Rejection.id == rejection_id).values(**rejection_update.dict(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    return await get_rejection(db, rejection_id)

async def delete_rejection(db: AsyncSession, rejection_id: int):
    await db.execute(delete(Rejection).where(Rejection.id == rejection_id))
    await db.commit()