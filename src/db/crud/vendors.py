# src/db/crud/vendors.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.vendors import Vendor
from src.db.schemas.vendors import VendorCreate, VendorUpdate
from typing import List

async def create_vendor(db: AsyncSession, vendor: VendorCreate):
    mandatory_fields = ["name", "contact_no", "address1", "city", "state", "state_code", "pin"]
    if not all(getattr(vendor, field) for field in mandatory_fields):
        raise ValueError("All mandatory fields are required")
    db_vendor = Vendor(**vendor.dict())
    db.add(db_vendor)
    await db.commit()
    await db.refresh(db_vendor)
    return db_vendor

async def get_vendors(db: AsyncSession) -> List[Vendor]:
    result = await db.execute(select(Vendor))
    return result.scalars().all()

async def get_vendor(db: AsyncSession, vendor_id: int):
    result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
    return result.scalar_one_or_none()

async def update_vendor(db: AsyncSession, vendor_id: int, vendor_update: VendorUpdate):
    stmt = update(Vendor).where(Vendor.id == vendor_id).values(**vendor_update.dict(exclude_unset=True))
    await db.execute(stmt)
    await db.commit()
    return await get_vendor(db, vendor_id)

async def delete_vendor(db: AsyncSession, vendor_id: int):
    stmt = delete(Vendor).where(Vendor.id == vendor_id)
    await db.execute(stmt)
    await db.commit()