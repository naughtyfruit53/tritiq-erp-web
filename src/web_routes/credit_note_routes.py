# src/web_routes/credit_note_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.db import get_db
from src.db.crud.credit_notes import get_credit_notes, get_credit_note, create_credit_note, update_credit_note, delete_credit_note
from src.db.crud.customers import get_customers
from src.db.crud.products import get_products
from src.db.schemas.credit_notes import CreditNoteCreate, CreditNoteUpdate, CnItemCreate, CnItemUpdate
from src.services.pdf import generate_credit_note_pdf
from .user_routes import get_current_user
import json

credit_note_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@credit_note_router.get("/credit_notes")
async def credit_notes_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    credit_notes = await get_credit_notes(db)
    customers = await get_customers(db)
    products = await get_products(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("credit_notes.html", {"request": request, "credit_notes": credit_notes, "customers": customers, "products": products, "today": today, "current_user": current_user})

@credit_note_router.post("/credit_notes")
async def create_credit_note_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    credit_note = CreditNoteCreate(
        cn_number=form['cn_number'],
        cn_date=form['cn_date'],
        sales_inv_id=int(form.get('sales_inv_id')) if form.get('sales_inv_id') else None,
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        voucher_data=form.get('voucher_data'),
        items=[CnItemCreate(**item) for item in items]
    )
    await create_credit_note(db, credit_note)
    return RedirectResponse("/credit_notes", status_code=303)

@credit_note_router.post("/credit_notes/{cn_id}")
async def update_credit_note_post(cn_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    credit_note_update = CreditNoteUpdate(
        cn_number=form['cn_number'],
        cn_date=form['cn_date'],
        sales_inv_id=int(form.get('sales_inv_id')) if form.get('sales_inv_id') else None,
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        voucher_data=form.get('voucher_data'),
        items=[CnItemUpdate(**item) for item in items]
    )
    await update_credit_note(db, cn_id, credit_note_update)
    return RedirectResponse("/credit_notes", status_code=303)

@credit_note_router.get("/credit_notes/{cn_id}/delete")
async def delete_credit_note_get(cn_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_credit_note(db, cn_id)
    return RedirectResponse("/credit_notes", status_code=303)

@credit_note_router.get("/credit_notes/{cn_id}/pdf")
async def credit_note_pdf(cn_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_credit_note_pdf(cn_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"credit_note_{cn_id}.pdf")