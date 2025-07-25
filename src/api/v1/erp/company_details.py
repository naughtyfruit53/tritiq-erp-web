# src/api/v1/erp/company_details.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.company_details import create_company_detail, get_company_detail, update_company_detail
from src.db.schemas.company_details import CompanyDetailCreate, CompanyDetailInDB, CompanyDetailUpdate

router = APIRouter()

@router.post("/", response_model=CompanyDetailInDB)
async def create_company(company: CompanyDetailCreate, db: AsyncSession = Depends(get_db)):
    return await create_company_detail(db, company)

@router.get("/", response_model=CompanyDetailInDB)
async def read_company(db: AsyncSession = Depends(get_db)):
    company = await get_company_detail(db)
    if company is None:
        raise HTTPException(status_code=404, detail="Company details not found")
    return company

@router.put("/", response_model=CompanyDetailInDB)
async def update_company(company: CompanyDetailUpdate, db: AsyncSession = Depends(get_db)):
    updated_company = await update_company_detail(db, 1, company)
    if updated_company is None:
        raise HTTPException(status_code=404, detail="Company details not found")
    return updated_company