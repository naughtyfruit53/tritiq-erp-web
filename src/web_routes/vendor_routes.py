# src/web_routes/vendor_routes.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse  # Moved to correct import
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.vendors import get_vendors, create_vendor
from src.db.schemas.vendors import VendorCreate
from .user_routes import get_current_user

vendor_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@vendor_router.get("/vendors")
async def vendors_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    vendors = await get_vendors(db)
    return templates.TemplateResponse("vendors.html", {"request": request, "vendors": vendors, "current_user": current_user})

@vendor_router.post("/vendors")
async def create_vendor_post(
    name: str = Form(...),
    contact_no: str = Form(...),
    address1: str = Form(None),
    address2: str = Form(None),
    city: str = Form(None),
    state: str = Form(None),
    state_code: str = Form(None),
    pin: str = Form(None),
    gst_no: str = Form(None),
    pan_no: str = Form(None),
    email: str = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    vendor_create = VendorCreate(
        name=name,
        contact_no=contact_no,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        state_code=state_code,
        pin=pin,
        gst_no=gst_no,
        pan_no=pan_no,
        email=email
    )
    await create_vendor(db, vendor_create)  # Assume this CRUD function exists; add if not
    return JSONResponse(status_code=200, content={"success": True})

@vendor_router.get("/api/v1/erp/vendors/list")
async def get_vendors_list(db: AsyncSession = Depends(get_db)):
    vendors = await get_vendors(db)
    return [{"id": v.id, "name": v.name} for v in vendors]