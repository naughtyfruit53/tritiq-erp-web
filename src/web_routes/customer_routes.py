# src/web_routes/customer_routes.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse  # Moved to correct import
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.customers import get_customers, create_customer
from src.db.schemas.customers import CustomerCreate
from .user_routes import get_current_user

customer_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@customer_router.get("/customers")
async def customers_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    customers = await get_customers(db)
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers, "current_user": current_user})

@customer_router.post("/customers")
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
    await create_customer(db, customer_create)
    return JSONResponse(status_code=200, content={"success": True})

@customer_router.get("/api/v1/erp/customers/list")
async def get_customers_list(db: AsyncSession = Depends(get_db)):
    customers = await get_customers(db)
    return [{"id": c.id, "name": c.name} for c in customers]