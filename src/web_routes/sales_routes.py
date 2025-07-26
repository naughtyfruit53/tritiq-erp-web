# src/web_routes/sales_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.db import get_db
from src.db.crud.sales_orders import get_sales_orders, get_sales_order, create_sales_order, update_sales_order, delete_sales_order
from src.db.crud.sales_invoices import get_sales_invoices, get_sales_invoice, create_sales_invoice, update_sales_invoice, delete_sales_invoice
from src.db.crud.customers import get_customers
from src.db.schemas.sales_orders import SalesOrderCreate, SalesOrderUpdate, SalesOrderItemCreate, SalesOrderItemUpdate
from src.db.schemas.sales_invoices import SalesInvoiceCreate, SalesInvoiceUpdate, SalesInvItemCreate, SalesInvItemUpdate
from src.db.crud.products import get_products
from src.db.crud.voucher_types import get_voucher_types
from src.services.pdf import generate_sales_order_pdf, generate_sales_invoice_pdf
from .user_routes import get_current_user
import json

sales_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@sales_router.get("/sales_orders")
async def sales_orders_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    sales_orders = await get_sales_orders(db)
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "sales_order"]
    today = date.today().isoformat()
    return templates.TemplateResponse("sales_orders.html", {"request": request, "sales_orders": sales_orders, "customers": customers, "products": products, "voucher_types": voucher_types, "today": today, "current_user": current_user})

@sales_router.post("/sales_orders")
async def create_sales_order_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    sales_order = SalesOrderCreate(
        sales_order_number=form['sales_order_number'],
        customer_id=int(form['customer_id']),
        sales_order_date=form['sales_order_date'],
        delivery_date=form.get('delivery_date'),
        payment_terms=form.get('payment_terms'),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        items=[SalesOrderItemCreate(**item) for item in items]
    )
    await create_sales_order(db, sales_order)
    return RedirectResponse("/sales_orders", status_code=303)

@sales_router.post("/sales_orders/{sales_order_id}")
async def update_sales_order_post(sales_order_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    sales_order_update = SalesOrderUpdate(
        sales_order_number=form['sales_order_number'],
        customer_id=int(form['customer_id']),
        sales_order_date=form['sales_order_date'],
        delivery_date=form.get('delivery_date'),
        payment_terms=form.get('payment_terms'),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        items=[SalesOrderItemUpdate(**item) for item in items]
    )
    await update_sales_order(db, sales_order_id, sales_order_update)
    return RedirectResponse("/sales_orders", status_code=303)

@sales_router.get("/sales_orders/{sales_order_id}/delete")
async def delete_sales_order_get(sales_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_sales_order(db, sales_order_id)
    return RedirectResponse("/sales_orders", status_code=303)

@sales_router.get("/sales_orders/{sales_order_id}/pdf")
async def sales_order_pdf(sales_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_sales_order_pdf(sales_order_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"sales_order_{sales_order_id}.pdf")

@sales_router.get("/sales_invoices")
async def sales_invoices_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    sales_invoices = await get_sales_invoices(db)
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "sales_inv"]
    sales_orders = await get_sales_orders(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("sales_invoices.html", {"request": request, "sales_invoices": sales_invoices, "customers": customers, "products": products, "voucher_types": voucher_types, "sales_orders": sales_orders, "today": today, "current_user": current_user})

@sales_router.post("/sales_invoices")
async def create_sales_invoice_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    sales_invoice = SalesInvoiceCreate(
        sales_inv_number=form['sales_inv_number'],
        invoice_date=form['invoice_date'],
        sales_order_id=int(form.get('sales_order_id')) if form.get('sales_order_id') else None,
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        voucher_data=form.get('voucher_data'),
        items=[SalesInvItemCreate(**item) for item in items]
    )
    await create_sales_invoice(db, sales_invoice)
    return RedirectResponse("/sales_invoices", status_code=303)

@sales_router.post("/sales_invoices/{sales_invoice_id}")
async def update_sales_invoice_post(sales_invoice_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    sales_invoice_update = SalesInvoiceUpdate(
        sales_inv_number=form['sales_inv_number'],
        invoice_date=form['invoice_date'],
        sales_order_id=int(form.get('sales_order_id')) if form.get('sales_order_id') else None,
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form.get('voucher_type_id')) if form.get('voucher_type_id') else None,
        voucher_data=form.get('voucher_data'),
        items=[SalesInvItemUpdate(**item) for item in items]
    )
    await update_sales_invoice(db, sales_invoice_id, sales_invoice_update)
    return RedirectResponse("/sales_invoices", status_code=303)

@sales_router.get("/sales_invoices/{sales_invoice_id}/delete")
async def delete_sales_invoice_get(sales_invoice_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_sales_invoice(db, sales_invoice_id)
    return RedirectResponse("/sales_invoices", status_code=303)

@sales_router.get("/sales_invoices/{sales_invoice_id}/pdf")
async def sales_invoice_pdf(sales_invoice_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_sales_invoice_pdf(sales_invoice_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"sales_invoice_{sales_invoice_id}.pdf")