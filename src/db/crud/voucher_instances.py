from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.voucher_instances import VoucherInstance
from ..schemas.voucher_instances import (
    VoucherInstanceCreate, 
    VoucherInstanceUpdate,
    VoucherInstance
)
import json
from typing import List, Optional, Dict

async def create_voucher_instance(
    db: AsyncSession, 
    voucher_instance: VoucherInstanceCreate
) -> VoucherInstance:
    """
    Create a new voucher instance record
    """
    db_obj = VoucherInstance(
        voucher_type_id=voucher_instance.voucher_type_id,
        voucher_number=voucher_instance.voucher_number,
        data_json=json.dumps(voucher_instance.data_json),
        module_name=voucher_instance.module_name,
        record_id=voucher_instance.record_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_voucher_instances(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[VoucherInstance]:
    """
    Get multiple voucher instances with pagination
    """
    result = await db.execute(
        select(VoucherInstance)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_voucher_instance(
    db: AsyncSession,
    voucher_instance_id: int
) -> Optional[VoucherInstance]:
    """
    Get a single voucher instance by ID
    """
    result = await db.execute(
        select(VoucherInstance)
        .where(VoucherInstance.id == voucher_instance_id)
    )
    return result.scalar_one_or_none()

async def get_voucher_instances_by_type(
    db: AsyncSession,
    voucher_type_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[VoucherInstance]:
    """
    Get voucher instances by voucher type ID
    """
    result = await db.execute(
        select(VoucherInstance)
        .where(VoucherInstance.voucher_type_id == voucher_type_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_voucher_instance(
    db: AsyncSession,
    voucher_instance_id: int,
    voucher_instance_update: VoucherInstanceUpdate
) -> Optional[VoucherInstance]:
    """
    Update voucher instance details
    """
    existing = await get_voucher_instance(db, voucher_instance_id)
    if not existing:
        return None
    
    update_data = voucher_instance_update.model_dump(exclude_unset=True)
    if 'data_json' in update_data:
        update_data['data_json'] = json.dumps(update_data['data_json'])
    
    stmt = (
        update(VoucherInstance)
        .where(VoucherInstance.id == voucher_instance_id)
        .values(**update_data)
    )
    
    await db.execute(stmt)
    await db.commit()
    return await get_voucher_instance(db, voucher_instance_id)

async def delete_voucher_instance(
    db: AsyncSession,
    voucher_instance_id: int
) -> bool:
    """
    Delete a voucher instance record
    Returns True if deleted, False if not found
    """
    voucher_instance = await get_voucher_instance(db, voucher_instance_id)
    if not voucher_instance:
        return False
    
    stmt = delete(VoucherInstance).where(VoucherInstance.id == voucher_instance_id)
    await db.execute(stmt)
    await db.commit()
    return True

async def count_voucher_instances_by_type(
    db: AsyncSession,
    voucher_type_id: int
) -> int:
    """
    Count voucher instances for a specific voucher type
    """
    result = await db.execute(
        select(func.count(VoucherInstance.id))
        .where(VoucherInstance.voucher_type_id == voucher_type_id)
    )
    return result.scalar() or 0

async def get_voucher_instance_counts_by_types(
    db: AsyncSession,
    voucher_type_ids: List[int]
) -> Dict[int, int]:
    """
    Get instance counts for multiple voucher types efficiently
    Returns a dictionary mapping voucher_type_id to count
    """
    result = await db.execute(
        select(
            VoucherInstance.voucher_type_id,
            func.count(VoucherInstance.id).label('count')
        )
        .where(VoucherInstance.voucher_type_id.in_(voucher_type_ids))
        .group_by(VoucherInstance.voucher_type_id)
    )
    
    counts = {}
    for row in result:
        counts[row.voucher_type_id] = row.count
    
    # Ensure all requested type IDs have an entry (default to 0)
    for type_id in voucher_type_ids:
        if type_id not in counts:
            counts[type_id] = 0
    
    return counts