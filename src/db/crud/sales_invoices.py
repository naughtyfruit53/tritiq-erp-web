from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.sales_invoices import SalesInvoice
from src.db.models.sales_inv_items import SalesInvItem
from src.db.schemas.sales_invoices import SalesInvoiceCreate, SalesInvoiceUpdate, SalesInvoiceInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_sales_invoice(db: AsyncSession, sales_invoice: SalesInvoiceCreate) -> SalesInvoice:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "sales_invoice", fiscal_year)
    sales_invoice.sales_inv_number = f"SINV/{fiscal_year}/{seq:04d}"
    db_sales_invoice = SalesInvoice(**sales_invoice.dict(exclude={'items'}))
    db.add(db_sales_invoice)
    await db.commit()
    await db.refresh(db_sales_invoice)
    for item in sales_invoice.items:
        db_item = SalesInvItem(sales_inv_id=db_sales_invoice.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "sales_invoice", fiscal_year)
    await db.refresh(db_sales_invoice)
    return db_sales_invoice

async def get_sales_invoices(db: AsyncSession) -> List[SalesInvoice]:
    result = await db.execute(select(SalesInvoice))
    return result.scalars().all()

async def get_sales_invoice(db: AsyncSession, sales_invoice_id: int) -> Optional[SalesInvoice]:
    result = await db.execute(select(SalesInvoice).where(SalesInvoice.id == sales_invoice_id))
    sales_invoice = result.scalar_one_or_none()
    if sales_invoice:
        result_items = await db.execute(select(SalesInvItem).where(SalesInvItem.sales_inv_id == sales_invoice_id))
        sales_invoice.items = result_items.scalars().all()
    return sales_invoice

async def update_sales_invoice(db: AsyncSession, sales_invoice_id: int, sales_invoice_update: SalesInvoiceUpdate) -> Optional[SalesInvoice]:
    stmt = update(SalesInvoice).where(SalesInvoice.id == sales_invoice_id).values(**sales_invoice_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if sales_invoice_update.items is not None:
        await db.execute(delete(SalesInvItem).where(SalesInvItem.sales_inv_id == sales_invoice_id))
        for item in sales_invoice_update.items:
            db_item = SalesInvItem(sales_inv_id=sales_invoice_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_sales_invoice(db, sales_invoice_id)

async def delete_sales_invoice(db: AsyncSession, sales_invoice_id: int):
    await db.execute(delete(SalesInvItem).where(SalesInvItem.sales_inv_id == sales_invoice_id))
    await db.execute(delete(SalesInvoice).where(SalesInvoice.id == sales_invoice_id))
    await db.commit()