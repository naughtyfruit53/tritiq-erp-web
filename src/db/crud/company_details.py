# src/db/crud/company_details.py
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.company_details import CompanyDetail
from src.db.schemas.company_details import (
    CompanyDetailCreate,
    CompanyDetailUpdate,
    CompanyDetailInDB
)

async def create_company_detail(
    db: AsyncSession,
    company_detail: CompanyDetailCreate
) -> CompanyDetailInDB:
    """
    Create a new company detail record
    """
    db_company = CompanyDetail(**company_detail.model_dump())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def get_company_detail(
    db: AsyncSession,
    company_id: int | None = None
) -> CompanyDetailInDB | None:
    """
    Get a single company detail by ID or the first record if no ID provided
    """
    if company_id is not None:
        result = await db.execute(
            select(CompanyDetail).where(CompanyDetail.id == company_id)
        )
        return result.scalar_one_or_none()
    else:
        result = await db.execute(select(CompanyDetail).limit(1))
        return result.scalar_one_or_none()

async def update_company_detail(
    db: AsyncSession,
    company_id: int,
    company_detail: CompanyDetailUpdate
) -> CompanyDetailInDB | None:
    """
    Update company details
    """
    # Get existing values
    existing = await get_company_detail(db, company_id)
    if not existing:
        return None
    
    # Update only provided fields
    update_data = company_detail.model_dump(exclude_unset=True)
    stmt = (
        update(CompanyDetail)
        .where(CompanyDetail.id == company_id)
        .values(**update_data)
    )
    
    await db.execute(stmt)
    await db.commit()
    return await get_company_detail(db, company_id)

async def get_all_company_details(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> list[CompanyDetailInDB]:
    """
    Get all company details with pagination
    """
    result = await db.execute(
        select(CompanyDetail)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()