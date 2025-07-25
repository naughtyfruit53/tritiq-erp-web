# src/api/v1/crm/contacts.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.db import get_db
from src.db.crud.crm import get_contacts, create_contact
from src.db.schemas.crm import ContactCreate, Contact

router = APIRouter(prefix="/contacts", tags=["contacts"])

# Assuming templates are in a 'templates' directory at the project root
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def contacts_page(request: Request, db: AsyncSession = Depends(get_db)):
    contacts = await get_contacts(db)
    return templates.TemplateResponse("crm/contacts.html", {"request": request, "contacts": contacts})

@router.get("/create")
async def contacts_create_page(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("crm/contacts_form.html", {"request": request})

@router.post("/")
async def create_contact_post(request: Request, name: str = Form(...), email: Optional[str] = Form(None), phone: Optional[str] = Form(None), company: Optional[str] = Form(None), notes: Optional[str] = Form(None), db: AsyncSession = Depends(get_db)):
    contact = ContactCreate(name=name, email=email, phone=phone, company=company, notes=notes)
    await create_contact(db, contact)
    return RedirectResponse("/contacts", status_code=303)