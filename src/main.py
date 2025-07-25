# src/main.py
from fastapi import FastAPI, Request, Form, Depends, File, UploadFile, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1 import api_router
from src.db import get_db
from src.db.crud.users import get_users, create_user, get_user_by_username
from src.db.crud.company_details import get_company_detail, update_company_detail, create_company_detail
from src.db.crud.products import get_products
from src.db.crud.vendors import get_vendors
from src.db.crud.customers import get_customers, create_customer  # Assume create_customer exists; add if not
from src.db.crud.voucher_types import get_voucher_types
from src.db.crud.voucher_columns import get_voucher_columns
from src.db.crud.sales_orders import get_sales_orders, get_sales_order
from src.db.crud.sales_invoices import get_sales_invoices, get_sales_invoice
from src.db.crud.purchase_orders import get_purchase_orders, get_purchase_order
from src.db.crud.purchase_inv import get_purchase_invs, get_purchase_inv
from src.db.crud.sequences import get_next_sequence, increment_sequence
from src.db.crud.grn import get_grns, get_grn
from src.db.crud.rejections import get_rejections
from src.db.crud.stock import get_stocks
from src.db.crud.bom import get_boms
from src.db.crud.work_orders import get_work_orders, get_open_work_orders
from src.db.crud.material_transactions import get_material_transactions
from src.db.schemas.users import UserCreate
from src.db.schemas.company_details import CompanyDetailUpdate, CompanyDetailCreate
from src.db.schemas.customers import CustomerCreate  # Assume schema exists
from src.services.pdf import generate_sales_order_pdf, generate_sales_invoice_pdf, generate_purchase_order_pdf, generate_purchase_inv_pdf, generate_grn_pdf, generate_rejection_pdf
from datetime import date
import json
import logging
import bcrypt  # pip install bcrypt for password hashing
import uuid  # For simple session IDs
import os  # For logo upload path
import requests  # pip install requests for API calls

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

logging.basicConfig(filename='logs/erp_app.log', level=logging.DEBUG)

# Fake in-memory sessions for demo (use Redis or proper auth in production)
sessions: Dict[str, str] = {}  # session_id: username

# Directory for uploaded logos
LOGO_DIR = "src/static/logos"
os.makedirs(LOGO_DIR, exist_ok=True)

def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        return sessions[session_id]
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

@app.get("/")
async def root(request: Request, db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    if not users:
        return RedirectResponse("/setup")
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/setup")
async def setup_page(request: Request, db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    if users:
        return RedirectResponse("/")
    return templates.TemplateResponse("setup.html", {"request": request})  # Add setup.html with form POST to /setup

@app.post("/setup")
async def create_first_user(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    users = await get_users(db)
    if users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Setup already completed")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_create = UserCreate(username=username, password=hashed_password, role="admin", active=True, must_change_password=True)
    await create_user(db, user_create)
    return RedirectResponse("/", status_code=303)

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_username(db, username)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Create simple session
    session_id = str(uuid.uuid4())
    sessions[session_id] = username
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

@app.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        sessions.pop(session_id, None)
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session_id")
    return response

@app.get("/dashboard")
async def dashboard(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})

@app.get("/users")
async def users_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    users = await get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/company")
async def company_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    company = await get_company_detail(db)
    states_dict = {
        "Andaman and Nicobar Islands": "35",
        "Andhra Pradesh": "37",
        "Arunachal Pradesh": "12",
        "Assam": "18",
        "Bihar": "10",
        "Chandigarh": "04",
        "Chhattisgarh": "22",
        "Dadra and Nagar Haveli and Daman and Diu": "26",
        "Delhi": "07",
        "Goa": "30",
        "Gujarat": "24",
        "Haryana": "06",
        "Himachal Pradesh": "02",
        "Jammu and Kashmir": "01",
        "Jharkhand": "20",
        "Karnataka": "29",
        "Kerala": "32",
        "Ladakh": "38",
        "Lakshadweep": "31",
        "Madhya Pradesh": "23",
        "Maharashtra": "27",
        "Manipur": "14",
        "Meghalaya": "17",
        "Mizoram": "15",
        "Nagaland": "13",
        "Odisha": "21",
        "Other Territory": "97",
        "Puducherry": "34",
        "Punjab": "03",
        "Rajasthan": "08",
        "Sikkim": "11",
        "Tamil Nadu": "33",
        "Telangana": "36",
        "Tripura": "16",
        "Uttar Pradesh": "09",
        "Uttarakhand": "05",
        "West Bengal": "19"
    }
    states = list(states_dict.keys())
    return templates.TemplateResponse("company_details.html", {"request": request, "company": company, "states": states})

@app.post("/company")
async def update_company(
    company_name: str = Form(...),
    address1: str = Form(...),
    address2: Optional[str] = Form(None),
    city: str = Form(...),
    state: str = Form(...),
    pin: str = Form(...),
    state_code: str = Form(...),
    gst_no: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    contact_no: str = Form(...),
    email: Optional[str] = Form(None),
    logo: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    logo_path = None
    if logo:
        logo_filename = f"{uuid.uuid4()}_{logo.filename}"
        logo_path = os.path.join(LOGO_DIR, logo_filename)
        with open(logo_path, "wb") as f:
            f.write(await logo.read())
        logo_path = f"/static/logos/{logo_filename}"

    update_data = CompanyDetailUpdate(
        company_name=company_name,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        pin=pin,
        state_code=state_code,
        gst_no=gst_no,
        pan_no=pan_no,
        contact_no=contact_no,
        email=email,
        logo_path=logo_path if logo else None,
    )
    company = await get_company_detail(db)
    if company:
        await update_company_detail(db, company.id, update_data)
    else:
        create_data = CompanyDetailCreate(
            company_name=company_name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            pin=pin,
            state_code=state_code,
            gst_no=gst_no,
            pan_no=pan_no,
            contact_no=contact_no,
            email=email,
            logo_path=logo_path,
        )
        await create_company_detail(db, create_data)
    return RedirectResponse("/company", status_code=303)

@app.get("/api/lookup_pin")
async def lookup_pin(pin: str):
    try:
        response = requests.get(f"https://api.postalpincode.in/pincode/{pin}")
        data = response.json()
        return data[0]  # Return the first result for simplicity
    except Exception as e:
        logging.error(f"PIN lookup failed: {e}")
        raise HTTPException(status_code=500, detail="PIN lookup failed")

@app.get("/api/lookup_gst")
async def lookup_gst(gst: str):
    # Placeholder for GST API (replace with real API if available)
    return {"success": False, "message": "GST API not implemented"}

@app.get("/products")
async def products_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    products = await get_products(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.get("/vendors")
async def vendors_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    vendors = await get_vendors(db)
    return templates.TemplateResponse("vendors.html", {"request": request, "vendors": vendors})

@app.get("/customers")
async def customers_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    customers = await get_customers(db)
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@app.get("/add_customer")
async def add_customer_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Form for adding customer
    return templates.TemplateResponse("add_customer.html", {"request": request})

@app.post("/customers")
async def create_customer(
    name: str = Form(...),
    contact_no: str = Form(...),
    address1: str = Form(None),
    address2: str = Form(None),
    city: str = Form(None),
    state: str = Form(None),
    state_code: str = Form(None),
    pin: str = Form(None),
    gst_no: str = Form(None),
    pan_no: str = Form(None),
    email: str = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    customer_create = CustomerCreate(
        name=name,
        contact_no=contact_no,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        state_code=state_code,
        pin=pin,
        gst_no=gst_no,
        pan_no=pan_no,
        email=email
    )
    await create_customer(db, customer_create)  # Assume this CRUD function exists; add if not
    return RedirectResponse("/customers", status_code=303)

@app.get("/voucher_types")
async def voucher_types_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    voucher_types = await get_voucher_types(db)
    return templates.TemplateResponse("voucher_types.html", {"request": request, "voucher_types": voucher_types})

@app.get("/voucher_columns/{voucher_type_id}")
async def voucher_columns_page(request: Request, voucher_type_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    voucher_columns = await get_voucher_columns(db, voucher_type_id)
    return templates.TemplateResponse("voucher_columns.html", {"request": request, "voucher_columns": voucher_columns, "voucher_type_id": voucher_type_id})

@app.get("/sales_orders")
async def sales_orders_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    sales_orders = await get_sales_orders(db)
    return templates.TemplateResponse("sales_orders.html", {"request": request, "sales_orders": sales_orders})

@app.get("/sales_orders/create")
async def sales_order_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "sales_order"]
    today = date.today().isoformat()
    return templates.TemplateResponse("sales_order_form.html", {"request": request, "customers": customers, "products": products, "voucher_types": voucher_types, "today": today})

@app.post("/sales_orders")
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
        voucher_type_id=int(form['voucher_type_id']) if form.get('voucher_type_id') else None,
        items=[SalesOrderItemCreate(**item) for item in items]
    )
    await create_sales_order(db, sales_order)
    return RedirectResponse("/sales_orders", status_code=303)

@app.get("/sales_orders/{sales_order_id}/edit")
async def sales_order_edit_page(sales_order_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    data = await get_sales_order(db, sales_order_id)
    if not data:
        raise HTTPException(status_code=404, detail="Sales Order not found")
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "sales_order"]
    today = date.today().isoformat()
    return templates.TemplateResponse("sales_order_form.html", {"request": request, "data": data, "customers": customers, "products": products, "voucher_types": voucher_types, "today": today})

@app.post("/sales_orders/{sales_order_id}")
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
        voucher_type_id=int(form['voucher_type_id']) if form.get('voucher_type_id') else None,
        items=[SalesOrderItemUpdate(**item) for item in items]
    )
    await update_sales_order(db, sales_order_id, sales_order_update)
    return RedirectResponse("/sales_orders", status_code=303)

@app.get("/sales_orders/{sales_order_id}/delete")
async def delete_sales_order_get(sales_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_sales_order(db, sales_order_id)
    return RedirectResponse("/sales_orders", status_code=303)

@app.get("/sales_orders/{sales_order_id}/pdf")
async def sales_order_pdf(sales_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_sales_order_pdf(sales_order_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"sales_order_{sales_order_id}.pdf")

@app.get("/sales_invoices")
async def sales_invoices_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    sales_invoices = await get_sales_invoices(db)
    return templates.TemplateResponse("sales_invoices.html", {"request": request, "sales_invoices": sales_invoices})

@app.get("/sales_invoices/create")
async def sales_invoice_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "sales_inv"]
    sales_orders = await get_sales_orders(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("sales_invoice_form.html", {"request": request, "customers": customers, "products": products, "voucher_types": voucher_types, "sales_orders": sales_orders, "today": today})

@app.post("/sales_invoices")
async def create_sales_invoice_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    sales_invoice = SalesInvoiceCreate(
        sales_inv_number=form['sales_inv_number'],
        invoice_date=form['invoice_date'],
        sales_order_id=int(form['sales_order_id']) if form['sales_order_id'] else None,
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form['voucher_type_id']) if form.get('voucher_type_id') else None,
        voucher_data=form.get('voucher_data'),
        items=[SalesInvItemCreate(**item) for item in items]
    )
    await create_sales_invoice(db, sales_invoice)
    return RedirectResponse("/sales_invoices", status_code=303)

@app.get("/sales_invoices/{sales_invoice_id}/edit")
async def sales_invoice_edit_page(sales_invoice_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    data = await get_sales_invoice(db, sales_invoice_id)
    if not data:
        raise HTTPException(status_code=404, detail="Sales Invoice not found")
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "sales_inv"]
    sales_orders = await get_sales_orders(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("sales_invoice_form.html", {"request": request, "data": data, "customers": customers, "products": products, "voucher_types": voucher_types, "sales_orders": sales_orders, "today": today})

@app.post("/sales_invoices/{sales_invoice_id}")
async def update_sales_invoice_post(sales_invoice_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    sales_invoice_update = SalesInvoiceUpdate(
        sales_inv_number=form['sales_inv_number'],
        invoice_date=form['invoice_date'],
        sales_order_id=int(form['sales_order_id']) if form['sales_order_id'] else None,
        customer_id=int(form['customer_id']),
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form['voucher_type_id']) if form['voucher_type_id'] else None,
        voucher_data=form.get('voucher_data'),
        items=[SalesInvItemUpdate(**item) for item in items]
    )
    await update_sales_invoice(db, sales_invoice_id, sales_invoice_update)
    return RedirectResponse("/sales_invoices", status_code=303)

@app.get("/sales_invoices/{sales_invoice_id}/delete")
async def delete_sales_invoice_get(sales_invoice_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_sales_invoice(db, sales_invoice_id)
    return RedirectResponse("/sales_invoices", status_code=303)

@app.get("/sales_invoices/{sales_invoice_id}/pdf")
async def sales_invoice_pdf(sales_invoice_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_sales_invoice_pdf(sales_invoice_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"sales_invoice_{sales_invoice_id}.pdf")

@app.get("/purchase_orders")
async def purchase_orders_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    purchase_orders = await get_purchase_orders(db)
    return templates.TemplateResponse("purchase_orders.html", {"request": request, "purchase_orders": purchase_orders})

@app.get("/purchase_orders/create")
async def purchase_order_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    vendors = await get_vendors(db)
    products = await get_products(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("purchase_order_form.html", {"request": request, "vendors": vendors, "products": products, "today": today})

@app.post("/purchase_orders")
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

@app.get("/purchase_orders/{purchase_order_id}/edit")
async def purchase_order_edit_page(purchase_order_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    data = await get_purchase_order(db, purchase_order_id)
    if not data:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    vendors = await get_vendors(db)
    products = await get_products(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("purchase_order_form.html", {"request": request, "data": data, "vendors": vendors, "products": products, "today": today})

@app.post("/purchase_orders/{purchase_order_id}")
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

@app.get("/purchase_orders/{purchase_order_id}/delete")
async def delete_purchase_order_get(purchase_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_purchase_order(db, purchase_order_id)
    return RedirectResponse("/purchase_orders", status_code=303)

@app.get("/purchase_orders/{purchase_order_id}/pdf")
async def purchase_order_pdf(purchase_order_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_purchase_order_pdf(purchase_order_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"purchase_order_{purchase_order_id}.pdf")

@app.get("/purchase_invoices")
async def purchase_invoices_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    purchase_invoices = await get_purchase_invs(db)
    return templates.TemplateResponse("purchase_invoices.html", {"request": request, "purchase_invoices": purchase_invoices})

@app.get("/purchase_invoices/create")
async def purchase_invoice_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    purchase_orders = await get_purchase_orders(db)
    vendors = await get_vendors(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "purchase_inv"]
    today = date.today().isoformat()
    return templates.TemplateResponse("purchase_invoice_form.html", {"request": request, "purchase_orders": purchase_orders, "vendors": vendors, "products": products, "voucher_types": voucher_types, "today": today})

@app.post("/purchase_invoices")
async def create_purchase_invoice_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    purchase_inv = PurchaseInvCreate(
        pur_inv_number=form['pur_inv_number'],
        invoice_number=form['invoice_number'],
        invoice_date=form['invoice_date'],
        grn_id=int(form['grn_id']) if form['grn_id'] else None,
        po_id=int(form['po_id']),
        vendor_id=int(form['vendor_id']),
        pur_inv_date=form['pur_inv_date'],
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form['voucher_type_id']) if form.get('voucher_type_id') else None,
        items=[PurchaseInvItemCreate(**item) for item in items]
    )
    await create_purchase_inv(db, purchase_inv)
    return RedirectResponse("/purchase_invoices", status_code=303)

@app.get("/purchase_invoices/{purchase_inv_id}/edit")
async def purchase_invoice_edit_page(purchase_inv_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    data = await get_purchase_inv(db, purchase_inv_id)
    if not data:
        raise HTTPException(status_code=404, detail="Purchase Invoice not found")
    purchase_orders = await get_purchase_orders(db)
    vendors = await get_vendors(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "purchase_inv"]
    today = date.today().isoformat()
    return templates.TemplateResponse("purchase_invoice_form.html", {"request": request, "data": data, "purchase_orders": purchase_orders, "vendors": vendors, "products": products, "voucher_types": voucher_types, "today": today})

@app.post("/purchase_invoices/{purchase_inv_id}")
async def update_purchase_invoice_post(purchase_inv_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    purchase_inv_update = PurchaseInvUpdate(
        pur_inv_number=form['pur_inv_number'],
        invoice_number=form['invoice_number'],
        invoice_date=form['invoice_date'],
        grn_id=int(form['grn_id']) if form['grn_id'] else None,
        po_id=int(form['po_id']),
        vendor_id=int(form['vendor_id']),
        pur_inv_date=form['pur_inv_date'],
        total_amount=float(form['total_amount']),
        cgst_amount=float(form.get('cgst_amount')) if form.get('cgst_amount') else None,
        sgst_amount=float(form.get('sgst_amount')) if form.get('sgst_amount') else None,
        igst_amount=float(form.get('igst_amount')) if form.get('igst_amount') else None,
        voucher_type_id=int(form['voucher_type_id']) if form['voucher_type_id'] else None,
        items=[PurchaseInvItemUpdate(**item) for item in items]
    )
    await update_purchase_inv(db, purchase_inv_id, purchase_inv_update)
    return RedirectResponse("/purchase_invoices", status_code=303)

@app.get("/purchase_invoices/{purchase_inv_id}/delete")
async def delete_purchase_invoice_get(purchase_inv_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_purchase_inv(db, purchase_inv_id)
    return RedirectResponse("/purchase_invoices", status_code=303)

@app.get("/purchase_invoices/{purchase_inv_id}/pdf")
async def purchase_inv_pdf(purchase_inv_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_purchase_inv_pdf(purchase_inv_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"purchase_inv_{purchase_inv_id}.pdf")

@app.get("/quotations")
async def quotations_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    quotations = await get_quotations(db)
    return templates.TemplateResponse("quotations.html", {"request": request, "quotations": quotations})

@app.get("/quotations/create")
async def quotation_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    customers = await get_customers(db)
    products = await get_products(db)
    voucher_types = [vt for vt in await get_voucher_types(db) if vt.module_name == "quotation"]
    today = date.today().isoformat()
    return templates.TemplateResponse("quotation_form.html", {"request": request, "customers": customers, "products": products, "voucher_types": voucher_types, "today": today})

@app.post("/quotations")
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
        voucher_type_id=int(form['voucher_type_id']) if form.get('voucher_type_id') else None,
        items=[QuoteItemCreate(**item) for item in items]
    )
    await create_quotation(db, quotation)
    return RedirectResponse("/quotations", status_code=303)

# Add similar for quotation edit, delete, pdf

@app.get("/proforma_invoices")
async def proforma_invoices_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    proforma_invoices = await get_proforma_invoices(db)
    return templates.TemplateResponse("proforma_invoices.html", {"request": request, "proforma_invoices": proforma_invoices})

# Add similar for proforma create, post, edit, etc.

@app.get("/credit_notes")
async def credit_notes_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    credit_notes = await get_credit_notes(db)
    return templates.TemplateResponse("credit_notes.html", {"request": request, "credit_notes": credit_notes})

# Add similar for credit_note create, post, edit, etc.

@app.get("/pending")
async def pending_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    pendings = await get_pending(db)
    return templates.TemplateResponse("pending.html", {"request": request, "pendings": pendings})

@app.get("/delivery_challan")
async def delivery_challan_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    transactions = await get_material_transactions(db, type='Outflow')
    return templates.TemplateResponse("delivery_challan.html", {"request": request, "transactions": transactions})

@app.get("/delivery_challan/create")
async def delivery_challan_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    customers = await get_customers(db)
    products = await get_products(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("delivery_challan_form.html", {"request": request, "customers": customers, "products": products, "today": today})

@app.post("/delivery_challan")
async def create_delivery_challan_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    # Implement MaterialTransactionCreate with type='Outflow'
    # await create_material_transaction(db, transaction)
    return RedirectResponse("/delivery_challan", status_code=303)

@app.get("/grn")
async def grn_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    grns = await get_grns(db)
    return templates.TemplateResponse("grn.html", {"request": request, "grns": grns})

@app.get("/grn/create")
async def grn_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    purchase_orders = await get_purchase_orders(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("grn_form.html", {"request": request, "purchase_orders": purchase_orders, "today": today})

@app.post("/grn")
async def create_grn_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    grn = GrnCreate(
        po_id=int(form['po_id']),
        grn_number=form['grn_number'],
        description=form.get('description'),
        created_at=form['created_at'],
        status=form['status'],
        items=[GrnItemCreate(**item) for item in items]
    )
    await create_grn(db, grn)
    return RedirectResponse("/grn", status_code=303)

@app.get("/grn/{grn_id}/edit")
async def grn_edit_page(grn_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    data = await get_grn(db, grn_id)
    if not data:
        raise HTTPException(status_code=404, detail="GRN not found")
    purchase_orders = await get_purchase_orders(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("grn_form.html", {"request": request, "data": data, "purchase_orders": purchase_orders, "today": today})

@app.post("/grn/{grn_id}")
async def update_grn_post(grn_id: int, request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    grn_update = GrnUpdate(
        po_id=int(form['po_id']),
        grn_number=form['grn_number'],
        description=form.get('description'),
        created_at=form['created_at'],
        status=form['status'],
        items=[GrnItemUpdate(**item) for item in items]
    )
    await update_grn(db, grn_id, grn_update)
    return RedirectResponse("/grn", status_code=303)

@app.get("/grn/{grn_id}/delete")
async def delete_grn_get(grn_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_grn(db, grn_id)
    return RedirectResponse("/grn", status_code=303)

@app.get("/grn/{grn_id}/pdf")
async def grn_pdf(grn_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_grn_pdf(grn_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"grn_{grn_id}.pdf")

@app.get("/rejections")
async def rejections_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    rejections = await get_rejections(db)
    return templates.TemplateResponse("rejections.html", {"request": request, "rejections": rejections})

@app.get("/rejections/create")
async def rejection_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Placeholder, add grns, po_items, etc.
    return templates.TemplateResponse("rejection_form.html", {"request": request})

# Add similar for stock, bom, work_orders, etc.

@app.get("/stock")
async def stock_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    stocks = await get_stocks(db)
    return templates.TemplateResponse("stock.html", {"request": request, "stocks": stocks})

@app.get("/manufacturing")
async def manufacturing_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Placeholder
    return templates.TemplateResponse("manufacturing.html", {"request": request})

@app.get("/bom/create")
async def bom_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    products = await get_products(db)
    return templates.TemplateResponse("bom_form.html", {"request": request, "products": products})

@app.post("/bom")
async def create_bom_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    # Parse and create BOM
    return RedirectResponse("/manufacturing", status_code=303)

@app.get("/work_orders/create")
async def work_order_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    boms = await get_boms(db)
    return templates.TemplateResponse("work_order_form.html", {"request": request, "boms": boms})

@app.post("/work_orders")
async def create_work_order_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    # Parse and create work order
    return RedirectResponse("/manufacturing", status_code=303)

@app.get("/work_orders/close")
async def close_work_order_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    open_work_orders = await get_open_work_orders(db)
    return templates.TemplateResponse("close_work_order.html", {"request": request, "open_work_orders": open_work_orders})

@app.post("/work_orders/close")
async def close_work_order_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    # Parse and close work order
    return RedirectResponse("/manufacturing", status_code=303)

@app.get("/crm/leads")
async def crm_leads_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    leads = await get_leads(db)
    return templates.TemplateResponse("crm/leads.html", {"request": request, "leads": leads})

@app.get("/crm/leads/create")
async def crm_leads_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("crm/leads_form.html", {"request": request})

@app.get("/crm/contacts")
async def crm_contacts_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    contacts = await get_contacts(db)
    return templates.TemplateResponse("crm/contacts.html", {"request": request, "contacts": contacts})

@app.get("/crm/contacts/create")
async def crm_contacts_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("crm/contacts_form.html", {"request": request})

@app.get("/crm/tickets")
async def crm_tickets_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    tickets = await get_tickets(db)
    return templates.TemplateResponse("crm/tickets.html", {"request": request, "tickets": tickets})

@app.get("/crm/tickets/create")
async def crm_tickets_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    contacts = await get_contacts(db)
    return templates.TemplateResponse("crm/tickets_form.html", {"request": request, "contacts": contacts})

@app.get("/crm/follow_ups")
async def crm_follow_ups_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    follow_ups = await get_follow_ups(db)
    return templates.TemplateResponse("crm/follow_ups.html", {"request": request, "follow_ups": follow_ups})

@app.get("/crm/follow_ups/create")
async def crm_follow_ups_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    leads = await get_leads(db)
    return templates.TemplateResponse("crm/follow_ups_form.html", {"request": request, "leads": leads})

@app.get("/backup")
async def backup_page(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("backup.html", {"request": request})

@app.post("/backup/create")
async def create_backup_post(db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await create_backup(db)
    return FileResponse(path, media_type="application/octet-stream", filename="erp_backup.sql")

@app.post("/backup/restore")
async def restore_post(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await perform_restore(db, file)
    return {"message": "Restore completed successfully"}