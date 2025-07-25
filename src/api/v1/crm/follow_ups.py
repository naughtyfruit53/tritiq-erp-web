# src/api/v1/crm/follow_ups.py
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.crm import get_follow_ups, create_follow_up
from src.db.schemas.crm import FollowUpCreate, FollowUp
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/follow_ups", tags=["follow_ups"])

@router.get("/")
async def follow_ups_page(request: Request, db: AsyncSession = Depends(get_db)):
    follow_ups = await get_follow_ups(db)
    return templates.TemplateResponse("crm/follow_ups.html", {"request": request, "follow_ups": follow_ups})

@router.get("/create")
async def follow_ups_create_page(request: Request, db: AsyncSession = Depends(get_db)):
    leads = await get_leads(db)
    return templates.TemplateResponse("crm/follow_ups_form.html", {"request": request, "leads": leads})

@router.post("/")
async def create_follow_up_post(lead_id: int = Form(...), description: Optional[str] = Form(None), date: Optional[str] = Form(None), db: AsyncSession = Depends(get_db)):
    follow_up_date = datetime.strptime(date, "%Y-%m-%dT%H:%M") if date else None
    follow_up = FollowUpCreate(lead_id=lead_id, description=description, date=follow_up_date)
    await create_follow_up(db, follow_up)
    return RedirectResponse("/follow_ups", status_code=303)