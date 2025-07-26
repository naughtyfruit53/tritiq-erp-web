# src/web_routes/product_routes.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse  # Moved to correct import
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.products import get_products, create_product
from src.db.schemas.products import ProductCreate
from .user_routes import get_current_user

product_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@product_router.get("/products")
async def products_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    products = await get_products(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products, "current_user": current_user})

@product_router.post("/products")
async def create_product_post(
    name: str = Form(...),
    hsn_code: str = Form(...),
    unit: str = Form(...),
    unit_price: float = Form(...),
    gst_rate: float = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    product_create = ProductCreate(name=name, hsn_code=hsn_code, unit=unit, unit_price=unit_price, gst_rate=gst_rate)
    await create_product(db, product_create)  # Assume this CRUD function exists; add if not
    return JSONResponse(status_code=200, content={"success": True})

@product_router.get("/api/v1/erp/products/list")
async def get_products_list(db: AsyncSession = Depends(get_db)):
    products = await get_products(db)
    return [{"id": p.id, "name": p.name} for p in products]