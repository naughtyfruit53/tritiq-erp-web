# src/web_routes/custom_voucher_routes.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.voucher_types import create_voucher_type
from .user_routes import get_current_user

custom_voucher_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@custom_voucher_router.get("/vouchers/create_custom")
async def create_custom_voucher(request: Request, module: str, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Render add custom voucher form, POST to add endpoint
    return templates.TemplateResponse("create_custom_voucher.html", {"request": request, "module": module, "current_user": current_user})

@custom_voucher_router.post("/vouchers/create_custom")
async def create_custom_voucher_post(
    name: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Add to voucher_types with category=module
    # Assume create_voucher_type crud
    await create_voucher_type(db, name, category=request.query_params.get('module'))
    return RedirectResponse("/", status_code=303)  # Or refresh menu somehow, but since middleware, reload page