# src/api/v1/crm/leads.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["leads"])

# Assuming templates are in a 'templates' directory at the project root
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def leads_page(request: Request):
    return templates.TemplateResponse("crm/leads.html", {"request": request})

# Add placeholder routes for create, edit, etc.