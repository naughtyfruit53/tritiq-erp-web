# src/voucher_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.voucher_types import get_voucher_types
from src.db.crud.voucher_columns import get_voucher_columns
from src.web_routes.user_routes import get_current_user

voucher_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@voucher_router.get("/voucher_types")
async def voucher_types_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    voucher_types = await get_voucher_types(db)
    return templates.TemplateResponse("voucher_types.html", {"request": request, "voucher_types": voucher_types})

@voucher_router.get("/voucher_columns/{voucher_type_id}")
async def voucher_columns_page(request: Request, voucher_type_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    voucher_columns = await get_voucher_columns(db, voucher_type_id)
    return templates.TemplateResponse("voucher_columns.html", {"request": request, "voucher_columns": voucher_columns, "voucher_type_id": voucher_type_id})