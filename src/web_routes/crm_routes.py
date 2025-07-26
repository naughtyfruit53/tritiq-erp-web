# src/web_routes/crm_routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.crm import get_leads, get_contacts, get_tickets, get_follow_ups
from .user_routes import get_current_user

crm_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@crm_router.get("/crm/leads")
async def crm_leads_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    leads = await get_leads(db)
    return templates.TemplateResponse("crm/leads.html", {"request": request, "leads": leads, "current_user": current_user})

@crm_router.get("/crm/leads/create")
async def crm_leads_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("crm/leads_form.html", {"request": request, "current_user": current_user})

@crm_router.get("/crm/contacts")
async def crm_contacts_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    contacts = await get_contacts(db)
    return templates.TemplateResponse("crm/contacts.html", {"request": request, "contacts": contacts, "current_user": current_user})

@crm_router.get("/crm/contacts/create")
async def crm_contacts_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("crm/contacts_form.html", {"request": request, "current_user": current_user})

@crm_router.get("/crm/tickets")
async def crm_tickets_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    tickets = await get_tickets(db)
    return templates.TemplateResponse("crm/tickets.html", {"request": request, "tickets": tickets, "current_user": current_user})

@crm_router.get("/crm/tickets/create")
async def crm_tickets_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    contacts = await get_contacts(db)
    return templates.TemplateResponse("crm/tickets_form.html", {"request": request, "contacts": contacts, "current_user": current_user})

@crm_router.get("/crm/follow_ups")
async def crm_follow_ups_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    follow_ups = await get_follow_ups(db)
    return templates.TemplateResponse("crm/follow_ups.html", {"request": request, "follow_ups": follow_ups, "current_user": current_user})

@crm_router.get("/crm/follow_ups/create")
async def crm_follow_ups_create_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    leads = await get_leads(db)
    return templates.TemplateResponse("crm/follow_ups_form.html", {"request": request, "leads": leads, "current_user": current_user})