# src/db/crud/voucher_types.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models.voucher_types import VoucherType
from src.db.schemas.voucher_types import (
    VoucherTypeCreate, 
    VoucherTypeUpdate,
    VoucherTypeInDB
)
from typing import List, Optional

async def create_voucher_type(
    db: AsyncSession, 
    voucher_type: VoucherTypeCreate
) -> VoucherTypeInDB:
    """
    Create a new voucher type record
    """
    db_voucher_type = VoucherType(**voucher_type.model_dump())
    db.add(db_voucher_type)
    await db.commit()
    await db.refresh(db_voucher_type)
    return db_voucher_type

async def get_voucher_types(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[VoucherTypeInDB]:
    """
    Get multiple voucher types with pagination
    """
    result = await db.execute(
        select(VoucherType)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_voucher_type(
    db: AsyncSession,
    voucher_type_id: int
) -> Optional[VoucherTypeInDB]:
    """
    Get a single voucher type by ID
    """
    result = await db.execute(
        select(VoucherType)
        .where(VoucherType.id == voucher_type_id)
    )
    return result.scalar_one_or_none()

async def get_voucher_type_by_name(
    db: AsyncSession,
    name: str
) -> Optional[VoucherTypeInDB]:
    """
    Get a single voucher type by name
    """
    result = await db.execute(
        select(VoucherType)
        .where(VoucherType.name == name)
    )
    return result.scalar_one_or_none()

async def update_voucher_type(
    db: AsyncSession,
    voucher_type_id: int,
    voucher_type_update: VoucherTypeUpdate
) -> Optional[VoucherTypeInDB]:
    """
    Update voucher type details
    """
    # Get existing voucher type
    existing = await get_voucher_type(db, voucher_type_id)
    if not existing:
        return None
    
    # Update only provided fields
    update_data = voucher_type_update.model_dump(exclude_unset=True)
    stmt = (
        update(VoucherType)
        .where(VoucherType.id == voucher_type_id)
        .values(**update_data)
    )
    
    await db.execute(stmt)
    await db.commit()
    return await get_voucher_type(db, voucher_type_id)

async def delete_voucher_type(
    db: AsyncSession,
    voucher_type_id: int
) -> bool:
    """
    Delete a voucher type record
    Returns True if deleted, False if not found
    """
    voucher_type = await get_voucher_type(db, voucher_type_id)
    if not voucher_type:
        return False
    
    stmt = delete(VoucherType).where(VoucherType.id == voucher_type_id)
    await db.execute(stmt)
    await db.commit()
    return True

async def get_default_voucher_type(
    db: AsyncSession
) -> Optional[VoucherTypeInDB]:
    """
    Get the default voucher type
    """
    result = await db.execute(
        select(VoucherType)
        .where(VoucherType.is_default == True)
    )
    return result.scalar_one_or_none()