# src/db/crud/voucher_columns.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.voucher_columns import VoucherColumn
from src.db.schemas.voucher_columns import VoucherColumnCreate, VoucherColumnUpdate
from typing import List

async def create_voucher_column(db: AsyncSession, voucher_column: VoucherColumnCreate):
    db_voucher_column = VoucherColumn(**voucher_column.dict())
    db.add(db_voucher_column)
    await db.commit()
    await db.refresh(db_voucher_column)
    return db_voucher_column

async def get_voucher_columns(db: AsyncSession, voucher_type_id: int) -> List[VoucherColumn]:
    result = await db.execute(select(VoucherColumn).where(VoucherColumn.voucher_type_id == voucher_type_id))
    return result.scalars().all()

async def get_voucher_column(db: AsyncSession, voucher_column_id: int):
    result = await db.execute(select(VoucherColumn).where(VoucherColumn.id == voucher_column_id))
    return result.scalar_one_or_none()

async def update_voucher_column(db: AsyncSession, voucher_column_id: int, voucher_column_update: VoucherColumnUpdate):
    stmt = update(VoucherColumn).where(VoucherColumn.id == voucher_column_id).values(**voucher_column_update.dict(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    return await get_voucher_column(db, voucher_column_id)

async def delete_voucher_column(db: AsyncSession, voucher_column_id: int):
    stmt = delete(VoucherColumn).where(VoucherColumn.id == voucher_column_id)
    await db.execute(stmt)
    await db.commit()