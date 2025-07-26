# src/db/crud/proforma_invoices.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.proforma_invoice import ProformaInvoice
from src.db.models.proforma_invoice_items import ProformaInvoiceItem
from src.db.schemas.proforma_invoice import ProformaInvoiceCreate, ProformaInvoiceUpdate, ProformaInvoiceInDB
from src.db.crud.sequences import get_next_sequence, increment_sequence
from datetime import datetime
from typing import List, Optional

async def create_proforma_invoice(db: AsyncSession, proforma_invoice: ProformaInvoiceCreate) -> ProformaInvoice:
    fiscal_year = datetime.now().strftime("%Y")
    seq = await get_next_sequence(db, "proforma_invoice", fiscal_year)
    proforma_invoice.proforma_inv_number = f"PI/{fiscal_year}/{seq:04d}"
    db_proforma_invoice = ProformaInvoice(**proforma_invoice.dict(exclude={'items'}))
    db.add(db_proforma_invoice)
    await db.commit()
    await db.refresh(db_proforma_invoice)
    for item in proforma_invoice.items:
        db_item = ProformaInvoiceItem(proforma_inv_id=db_proforma_invoice.id, **item.dict())
        db.add(db_item)
    await db.commit()
    await increment_sequence(db, "proforma_invoice", fiscal_year)
    await db.refresh(db_proforma_invoice)
    return db_proforma_invoice

async def get_proforma_invoices(db: AsyncSession) -> List[ProformaInvoice]:
    result = await db.execute(select(ProformaInvoice))
    return result.scalars().all()

async def get_proforma_invoice(db: AsyncSession, proforma_invoice_id: int) -> Optional[ProformaInvoice]:
    result = await db.execute(select(ProformaInvoice).where(ProformaInvoice.id == proforma_invoice_id))
    proforma_invoice = result.scalar_one_or_none()
    if proforma_invoice:
        result_items = await db.execute(select(ProformaInvoiceItem).where(ProformaInvoiceItem.proforma_inv_id == proforma_invoice_id))
        proforma_invoice.items = result_items.scalars().all()
    return proforma_invoice

async def update_proforma_invoice(db: AsyncSession, proforma_invoice_id: int, proforma_invoice_update: ProformaInvoiceUpdate) -> Optional[ProformaInvoice]:
    stmt = update(ProformaInvoice).where(ProformaInvoice.id == proforma_invoice_id).values(**proforma_invoice_update.dict(exclude_unset=True, exclude={'items'}))
    await db.execute(stmt)
    await db.commit()
    if proforma_invoice_update.items is not None:
        await db.execute(delete(ProformaInvoiceItem).where(ProformaInvoiceItem.proforma_inv_id == proforma_invoice_id))
        for item in proforma_invoice_update.items:
            db_item = ProformaInvoiceItem(proforma_inv_id=proforma_invoice_id, **item.dict())
            db.add(db_item)
        await db.commit()
    return await get_proforma_invoice(db, proforma_invoice_id)

async def delete_proforma_invoice(db: AsyncSession, proforma_invoice_id: int):
    await db.execute(delete(ProformaInvoiceItem).where(ProformaInvoiceItem.proforma_inv_id == proforma_invoice_id))
    await db.execute(delete(ProformaInvoice).where(ProformaInvoice.id == proforma_invoice_id))
    await db.commit()