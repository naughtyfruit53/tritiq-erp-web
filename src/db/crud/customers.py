from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.customers import Customer
from src.db.schemas.customers import CustomerCreate, CustomerUpdate, CustomerInDB
from typing import List, Optional
from fastapi import HTTPException  # For raising API-friendly errors

async def create_customer(db: AsyncSession, customer: CustomerCreate) -> CustomerInDB:
    db_customer = Customer(**customer.dict())
    try:
        db.add(db_customer)
        await db.commit()
        await db.refresh(db_customer)
        return CustomerInDB.model_validate(db_customer)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Customer with this name already exists")

async def get_customers(
    db: AsyncSession,
    name: Optional[str] = None,
    gst_no: Optional[str] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "id",
    sort_desc: bool = False
) -> List[CustomerInDB]:
    query = select(Customer)
    if name:
        query = query.filter(Customer.name.ilike(f"%{name}%"))  # Case-insensitive partial match
    if gst_no:
        query = query.filter(Customer.gst_no == gst_no)
    if city:
        query = query.filter(Customer.city.ilike(f"%{city}%"))
    if sort_desc:
        query = query.order_by(getattr(Customer, sort_by).desc())
    else:
        query = query.order_by(getattr(Customer, sort_by))
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    customers = result.scalars().all()
    return [CustomerInDB.model_validate(c) for c in customers]

async def get_customer(db: AsyncSession, customer_id: int) -> Optional[CustomerInDB]:
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    db_customer = result.scalar_one_or_none()
    if db_customer:
        return CustomerInDB.model_validate(db_customer)
    return None

async def update_customer(db: AsyncSession, customer_id: int, customer_update: CustomerUpdate) -> Optional[CustomerInDB]:
    update_data = customer_update.dict(exclude_unset=True)
    if not update_data:
        return await get_customer(db, customer_id)  # No changes, return existing
    stmt = (
        update(Customer)
        .where(Customer.id == customer_id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
        .returning(Customer.id)
    )
    try:
        result = await db.execute(stmt)
        if result.rowcount == 0:
            return None
        await db.commit()
        return await get_customer(db, customer_id)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Update would violate unique constraint (e.g., duplicate name)")

async def delete_customer(db: AsyncSession, customer_id: int) -> bool:
    stmt = delete(Customer).where(Customer.id == customer_id).returning(Customer.id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0