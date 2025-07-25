# src/api/v1/crm/placeholders.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/leads")
async def get_leads():
    return {"message": "CRM Leads placeholder"}

@router.get("/contacts")
async def get_contacts():
    return {"message": "CRM Contacts placeholder"}

@router.get("/tickets")
async def get_tickets():
    return {"message": "CRM Tickets placeholder"}

@router.get("/followups")
async def get_followups():
    return {"message": "CRM Follow-ups placeholder"}