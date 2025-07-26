# src/web_routes/quotation_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.db import get_db
from src.db.crud.quotations import get_quotations, get_quotation, create_quotation, update_quotation, delete_quotation
from src.db.crud.customers import get_customers
from src.db.crud.products import get_products
from src.db.crud.voucher_types import get_voucher_types
from src.db.schemas.quotations import QuoteCreate, QuoteUpdate, QuoteItemCreate, QuoteItemUpdate
from src.services.pdf import generate_quotation_pdf
from .user_routes import get_current_user
import json

quotation_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@quotation_router.get("/quotations")
async def quotations_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    quotations = await get_quotations(db)
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "quotation"]
    today = date.today().isoformat()
    return templates.TemplateResponse("quotations.html", {"request": request, "quotations": quotations, "customers": customers, "products": products, "voucher_types": voucher_types, "today": today, "current_user": current_user})

@quotation_router.post("/quotations")
async def create_quotation_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    quotation = QuoteCreate(
        quotation_number=form['quotation_number'],
        customer_id=int(form['customer_id']),
        quotation_date=form['quotation_date'],
        validity_date=form.get('validity_date'),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        payment_terms=form.get('payment_terms'),
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        items=[QuoteItemCreate(**item) for item in items]
    )
    await create_quotation(db, quotation)
    return RedirectResponse("/quotations", status_code=303)

@quotation_router.post("/quotations/{quotation_id}")
async def update_quotation_post(quotation_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    quotation_update = QuoteUpdate(
        quotation_number=form['quotation_number'],
        customer_id=int(form['customer_id']),
        quotation_date=form['quotation_date'],
        validity_date=form.get('validity_date'),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        payment_terms=form.get('payment_terms'),
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        items=[QuoteItemUpdate(**item) for item in items]
    )
    await update_quotation(db, quotation_id, quotation_update)
    return RedirectResponse("/quotations", status_code=303)

@quotation_router.get("/quotations/{quotation_id}/delete")
async def delete_quotation_get(quotation_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_quotation(db, quotation_id)
    return RedirectResponse("/quotations", status_code=303)

@quotation_router.get("/quotations/{quotation_id}/pdf")
async def quotation_pdf(quotation_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_quotation_pdf(quotation_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"quotation_{quotation_id}.pdf")