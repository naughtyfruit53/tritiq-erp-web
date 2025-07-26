# src/web_routes/pending_routes.py
from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.pending import get_pending, filter_pending
from .user_routes import get_current_user

pending_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@pending_router.get("/pending")
async def pending_page(request: Request, search: str = Query(None), db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    if search:
        pendings = await filter_pending(db, search)
    else:
        pendings = await get_pending(db)
    return templates.TemplateResponse("pending.html", {"request": request, "pendings": pendings, "current_user": current_user})