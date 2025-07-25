from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.sales_invoices import create_sales_invoice, get_sales_invoices, get_sales_invoice, update_sales_invoice, delete_sales_invoice
from src.db.schemas.sales_invoices import SalesInvoiceCreate, SalesInvoiceInDB, SalesInvoiceUpdate

router = APIRouter(tags=["sales_invoices"])

@router.post("/", response_model=SalesInvoiceInDB)
async def create_new_sales_invoice(sales_invoice: SalesInvoiceCreate, db: AsyncSession = Depends(get_db)):
    return await create_sales_invoice(db, sales_invoice)

@router.get("/", response_model=List[SalesInvoiceInDB])
async def read_sales_invoices(db: AsyncSession = Depends(get_db)):
    return await get_sales_invoices(db)

@router.get("/{sales_invoice_id}", response_model=SalesInvoiceInDB)
async def read_sales_invoice(sales_invoice_id: int, db: AsyncSession = Depends(get_db)):
    db_sales_invoice = await get_sales_invoice(db, sales_invoice_id)
    if db_sales_invoice is None:
        raise HTTPException(status_code=404, detail="Sales Invoice not found")
    return db_sales_invoice

@router.put("/{sales_invoice_id}", response_model=SalesInvoiceInDB)
async def update_existing_sales_invoice(sales_invoice_id: int, sales_invoice: SalesInvoiceUpdate, db: AsyncSession = Depends(get_db)):
    db_sales_invoice = await update_sales_invoice(db, sales_invoice_id, sales_invoice)
    if db_sales_invoice is None:
        raise HTTPException(status_code=404, detail="Sales Invoice not found")
    return db_sales_invoice

@router.delete("/{sales_invoice_id}")
async def delete_existing_sales_invoice(sales_invoice_id: int, db: AsyncSession = Depends(get_db)):
    await delete_sales_invoice(db, sales_invoice_id)
    return {"detail": "Sales Invoice deleted"}