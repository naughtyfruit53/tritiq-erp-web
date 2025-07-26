# src/web_routes/delivery_challan_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.db import get_db
from src.db.crud.material_transactions import get_material_transactions, create_material_transaction
from src.db.schemas.material_transactions import MaterialTransactionCreate
from src.db.crud.customers import get_customers
from src.db.crud.products import get_products
from .user_routes import get_current_user
import json

delivery_challan_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@delivery_challan_router.get("/delivery_challan")
async def delivery_challan_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    transactions = await get_material_transactions(db, type='Outflow')
    customers = await get_customers(db)
    products = await get_products(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("delivery_challan.html", {"request": request, "transactions": transactions, "customers": customers, "products": products, "today": today, "current_user": current_user})

@delivery_challan_router.post("/delivery_challan")
async def create_delivery_challan_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    items_json = form['items_json']
    items = json.loads(items_json)
    # Implement MaterialTransactionCreate with type='Outflow'
    transaction = MaterialTransactionCreate(
        # Add fields as per schema, including type='Outflow'
    )
    await create_material_transaction(db, transaction)
    return RedirectResponse("/delivery_challan", status_code=303)