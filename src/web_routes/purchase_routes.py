# src/web_routes/purchase_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.db import get_db
from src.db.crud.purchase_orders import get_purchase_orders, get_purchase_order, create_purchase_order, update_purchase_order, delete_purchase_order
from src.db.crud.purchase_inv import get_purchase_invs, get_purchase_inv, create_purchase_inv, update_purchase_inv, delete_purchase_inv
from src.db.crud.vendors import get_vendors
from src.db.crud.products import get_products
from src.db.crud.voucher_types import get_voucher_types
from src.db.schemas.purchase_orders import PurchaseOrderCreate, PurchaseOrderUpdate, PoItemCreate, PoItemUpdate
from src.db.schemas.purchase_inv import PurchaseInvCreate, PurchaseInvUpdate, PurchaseInvItemCreate, PurchaseInvItemUpdate
from src.services.pdf import generate_purchase_order_pdf, generate_purchase_inv_pdf
from .user_routes import get_current_user
import json

purchase_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@purchase_router.get("/purchase_orders")
async def purchase_orders_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    purchase_orders = await get_purchase_orders(db)
    vendors = await get_vendors(db)
    products = await get_products(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("purchase_orders.html", {"request": request, "purchase_orders": purchase_orders, "vendors": vendors, "products": products, "today": today, "current_user": current_user})

@purchase_router.post("/purchase_orders")
async def create_purchase_order_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    purchase_order = PurchaseOrderCreate(
        po_number=form['po_number'],
        vendor_id=int(form['vendor_id']),
        po_date=form['po_date'],
        delivery_date=form.get('delivery_date'),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        payment_terms=form.get('payment_terms'),
        items=[PoItemCreate(**item) for item in items]
    )
    await create_purchase_order(db, purchase_order)
    return RedirectResponse("/purchase_orders", status_code=303)

@purchase_router.post("/purchase_orders/{purchase_order_id}")
async def update_purchase_order_post(purchase_order_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    purchase_order_update = PurchaseOrderUpdate(
        po_number=form['po_number'],
        vendor_id=int(form['vendor_id']),
        po_date=form['po_date'],
        delivery_date=form.get('delivery_date'),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        payment_terms=form.get('payment_terms'),
        items=[PoItemUpdate(**item) for item in items]
    )
    await update_purchase_order(db, purchase_order_id, purchase_order_update)
    return RedirectResponse("/purchase_orders", status_code=303)

@purchase_router.get("/purchase_orders/{purchase_order_id}/delete")
async def delete_purchase_order_get(purchase_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_purchase_order(db, purchase_order_id)
    return RedirectResponse("/purchase_orders", status_code=303)

@purchase_router.get("/purchase_orders/{purchase_order_id}/pdf")
async def purchase_order_pdf(purchase_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_purchase_order_pdf(purchase_order_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"purchase_order_{purchase_order_id}.pdf")

@purchase_router.get("/purchase_invoices")
async def purchase_invoices_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    purchase_invoices = await get_purchase_invs(db)
    purchase_orders = await get_purchase_orders(db)
    vendors = await get_vendors(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "purchase_inv"]
    today = date.today().isoformat()
    return templates.TemplateResponse("purchase_invoices.html", {"request": request, "purchase_invoices": purchase_invoices, "purchase_orders": purchase_orders, "vendors": vendors, "products": products, "voucher_types": voucher_types, "today": today, "current_user": current_user})

@purchase_router.post("/purchase_invoices")
async def create_purchase_invoice_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    purchase_inv = PurchaseInvCreate(
        pur_inv_number=form['pur_inv_number'],
        invoice_number=form['invoice_number'],
        invoice_date=form['invoice_date'],
        grn_id=int(form.get('grn_id')) if form.get('grn_id') else None,
        po_id=int(form['po_id']),
        vendor_id=int(form['vendor_id']),
        pur_inv_date=form['pur_inv_date'],
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        items=[PurchaseInvItemCreate(**item) for item in items]
    )
    await create_purchase_inv(db, purchase_inv)
    return RedirectResponse("/purchase_invoices", status_code=303)

@purchase_router.post("/purchase_invoices/{purchase_inv_id}")
async def update_purchase_invoice_post(purchase_inv_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    purchase_inv_update = PurchaseInvUpdate(
        pur_inv_number=form['pur_inv_number'],
        invoice_number=form['invoice_number'],
        invoice_date=form['invoice_date'],
        grn_id=int(form.get('grn_id')) if form.get('grn_id') else None,
        po_id=int(form['po_id']),
        vendor_id=int(form['vendor_id']),
        pur_inv_date=form['pur_inv_date'],
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        items=[PurchaseInvItemUpdate(**item) for item in items]
    )
    await update_purchase_inv(db, purchase_inv_id, purchase_inv_update)
    return RedirectResponse("/purchase_invoices", status_code=303)

@purchase_router.get("/purchase_invoices/{purchase_inv_id}/delete")
async def delete_purchase_invoice_get(purchase_inv_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_purchase_inv(db, purchase_inv_id)
    return RedirectResponse("/purchase_invoices", status_code=303)

@purchase_router.get("/purchase_invoices/{purchase_inv_id}/pdf")
async def purchase_inv_pdf(purchase_inv_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_purchase_inv_pdf(purchase_inv_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"purchase_inv_{purchase_inv_id}.pdf")