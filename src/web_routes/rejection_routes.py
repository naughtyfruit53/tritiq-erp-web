# src/web_routes/rejection_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.rejections import get_rejections
from .user_routes import get_current_user

rejection_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@rejection_router.get("/rejections")
async def rejections_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    rejections = await get_rejections(db)
    return templates.TemplateResponse("rejections.html", {"request": request, "rejections": rejections, "current_user": current_user})

@rejection_router.get("/rejections/create")
async def rejection_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Placeholder, add grns, po_items, etc.
    return templates.TemplateResponse("rejection_form.html", {"request": request, "current_user": current_user})