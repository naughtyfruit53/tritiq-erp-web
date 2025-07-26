# src/web_routes/proforma_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.db import get_db
from src.db.crud.proforma_invoice import get_proforma_invoices, get_proforma_invoice, create_proforma_invoice, update_proforma_invoice, delete_proforma_invoice
from src.db.crud.customers import get_customers
from src.db.crud.products import get_products
from src.db.crud.voucher_types import get_voucher_types
from src.db.schemas.proforma_invoice import ProformaInvoiceCreate, ProformaInvoiceUpdate, ProformaInvItemCreate, ProformaInvItemUpdate
from src.services.pdf import generate_proforma_invoice_pdf
from .user_routes import get_current_user
import json

proforma_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@proforma_router.get("/proforma_invoices")
async def proforma_invoices_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    proforma_invoices = await get_proforma_invoices(db)
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "proforma_invoice"]
    today = date.today().isoformat()
    return templates.TemplateResponse("proforma_invoices.html", {"request": request, "proforma_invoices": proforma_invoices, "customers": customers, "products": products, "voucher_types": voucher_types, "today": today, "current_user": current_user})

@proforma_router.post("/proforma_invoices")
async def create_proforma_invoice_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    proforma_invoice = ProformaInvoiceCreate(
        proforma_inv_number=form['proforma_inv_number'],
        proforma_date=form['proforma_date'],
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        voucher_data=form.get('voucher_data'),
        items=[ProformaInvItemCreate(**item) for item in items]
    )
    await create_proforma_invoice(db, proforma_invoice)
    return RedirectResponse("/proforma_invoices", status_code=303)

@proforma_router.post("/proforma_invoices/{proforma_invoice_id}")
async def update_proforma_invoice_post(proforma_invoice_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    proforma_invoice_update = ProformaInvoiceUpdate(
        proforma_inv_number=form['proforma_inv_number'],
        proforma_date=form['proforma_date'],
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        voucher_data=form.get('voucher_data'),
        items=[ProformaInvItemUpdate(**item) for item in items]
    )
    await update_proforma_invoice(db, proforma_invoice_id, proforma_invoice_update)
    return RedirectResponse("/proforma_invoices", status_code=303)

@proforma_router.get("/proforma_invoices/{proforma_invoice_id}/delete")
async def delete_proforma_invoice_get(proforma_invoice_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_proforma_invoice(db, proforma_invoice_id)
    return RedirectResponse("/proforma_invoices", status_code=303)

@proforma_router.get("/proforma_invoices/{proforma_invoice_id}/pdf")
async def proforma_invoice_pdf(proforma_invoice_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_proforma_invoice_pdf(proforma_invoice_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"proforma_invoice_{proforma_invoice_id}.pdf")