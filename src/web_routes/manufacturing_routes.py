# src/web_routes/manufacturing_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.bom import get_boms
from src.db.crud.work_orders import get_work_orders, get_open_work_orders
from .user_routes import get_current_user

manufacturing_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@manufacturing_router.get("/manufacturing")
async def manufacturing_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Placeholder
    return templates.TemplateResponse("manufacturing.html", {"request": request, "current_user": current_user})

@manufacturing_router.get("/bom/create")
async def bom_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    products = await get_products(db)
    return templates.TemplateResponse("bom_form.html", {"request": request, "products": products, "current_user": current_user})

@manufacturing_router.post("/bom")
async def create_bom_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    # Parse and create BOM
    return RedirectResponse("/manufacturing", status_code=303)

@manufacturing_router.get("/work_orders/create")
async def work_order_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    boms = await get_boms(db)
    return templates.TemplateResponse("work_order_form.html", {"request": request, "boms": boms, "current_user": current_user})

@manufacturing_router.post("/work_orders")
async def create_work_order_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    # Parse and create work order
    return RedirectResponse("/manufacturing", status_code=303)

@manufacturing_router.get("/work_orders/close")
async def close_work_order_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    open_work_orders = await get_open_work_orders(db)
    return templates.TemplateResponse("close_work_order.html", {"request": request, "open_work_orders": open_work_orders, "current_user": current_user})

@manufacturing_router.post("/work_orders/close")
async def close_work_order_post(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    form = await request.form()
    # Parse and close work order
    return RedirectResponse("/manufacturing", status_code=303)