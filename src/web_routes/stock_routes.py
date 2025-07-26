# src/web_routes/stock_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.stock import get_stocks
from .user_routes import get_current_user

stock_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@stock_router.get("/stock")
async def stock_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    stocks = await get_stocks(db)
    return templates.TemplateResponse("stock.html", {"request": request, "stocks": stocks, "current_user": current_user})