# src/web_routes/grn_routes.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.db import get_db
from src.db.crud.grn import get_grns, get_grn, create_grn, update_grn, delete_grn
from src.db.crud.purchase_orders import get_purchase_orders
from src.db.schemas.grn import GrnCreate, GrnUpdate, GrnItemCreate, GrnItemUpdate
from src.services.pdf import generate_grn_pdf
from .user_routes import get_current_user
import json

grn_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@grn_router.get("/grn")
async def grn_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    grns = await get_grns(db)
    purchase_orders = await get_purchase_orders(db)
    today = date.today().isoformat()
    return templates.TemplateResponse("grn.html", {"request": request, "grns": grns, "purchase_orders": purchase_orders, "today": today, "current_user": current_user})

@grn_router.post("/grn")
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

@grn_router.post("/grn/{grn_id}")
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

@grn_router.get("/grn/{grn_id}/delete")
async def delete_grn_get(grn_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await delete_grn(db, grn_id)
    return RedirectResponse("/grn", status_code=303)

@grn_router.get("/grn/{grn_id}/pdf")
async def grn_pdf(grn_id: int, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await generate_grn_pdf(grn_id, db)
    return FileResponse(path, media_type="application/pdf", filename=f"grn_{grn_id}.pdf")