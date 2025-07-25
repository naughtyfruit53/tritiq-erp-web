# src/api/v1/crm/tickets.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.db import get_db
from src.db.crud.crm import get_tickets, create_ticket, get_contacts
from src.db.schemas.crm import TicketCreate, Ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

# Assuming templates are in a 'templates' directory at the project root
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def tickets_page(request: Request, db: AsyncSession = Depends(get_db)):
    tickets = await get_tickets(db)
    return templates.TemplateResponse("crm/tickets.html", {"request": request, "tickets": tickets})

@router.get("/create")
async def tickets_create_page(request: Request, db: AsyncSession = Depends(get_db)):
    contacts = await get_contacts(db)
    return templates.TemplateResponse("crm/tickets_form.html", {"request": request, "contacts": contacts})

@router.post("/")
async def create_ticket_post(request: Request, subject: str = Form(...), description: Optional[str] = Form(None), priority: Optional[str] = Form("Medium"), contact_id: Optional[int] = Form(None), db: AsyncSession = Depends(get_db)):
    ticket = TicketCreate(subject=subject, description=description, priority=priority, contact_id=contact_id)
    await create_ticket(db, ticket)
    return RedirectResponse("/tickets", status_code=303)