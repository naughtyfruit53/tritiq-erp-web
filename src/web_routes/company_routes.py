# src/web_routes/company_routes.py
from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.db import get_db
from src.db.crud.company_details import get_company_detail, update_company_detail, create_company_detail
from src.db.schemas.company_details import CompanyDetailUpdate, CompanyDetailCreate
from .user_routes import get_current_user  # Relative import since in same folder
import os
import uuid
import requests

company_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

# Directory for uploaded logos
LOGO_DIR = "src/static/logos"
os.makedirs(LOGO_DIR, exist_ok=True)

@company_router.get("/company")
async def company_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    company = await get_company_detail(db)
    states_dict = {
        "Andaman and Nicobar Islands": "35",
        "Andhra Pradesh": "37",
        "Arunachal Pradesh": "12",
        "Assam": "18",
        "Bihar": "10",
        "Chandigarh": "04",
        "Chhattisgarh": "22",
        "Dadra and Nagar Haveli and Daman and Diu": "26",
        "Delhi": "07",
        "Goa": "30",
        "Gujarat": "24",
        "Haryana": "06",
        "Himachal Pradesh": "02",
        "Jammu and Kashmir": "01",
        "Jharkhand": "20",
        "Karnataka": "29",
        "Kerala": "32",
        "Ladakh": "38",
        "Lakshadweep": "31",
        "Madhya Pradesh": "23",
        "Maharashtra": "27",
        "Manipur": "14",
        "Meghalaya": "17",
        "Mizoram": "15",
        "Nagaland": "13",
        "Odisha": "21",
        "Other Territory": "97",
        "Puducherry": "34",
        "Punjab": "03",
        "Rajasthan": "08",
        "Sikkim": "11",
        "Tamil Nadu": "33",
        "Telangana": "36",
        "Tripura": "16",
        "Uttar Pradesh": "09",
        "Uttarakhand": "05",
        "West Bengal": "19"
    }
    states = list(states_dict.keys())
    return templates.TemplateResponse("company_details.html", {"request": request, "company": company, "states": states, "current_user": current_user})

@company_router.post("/company")
async def update_company(
    company_name: str = Form(...),
    address1: str = Form(...),
    address2: Optional[str] = Form(None),
    city: str = Form(...),
    state: str = Form(...),
    pin: str = Form(...),
    state_code: str = Form(...),
    gst_no: Optional[str] = Form(None),
    pan_no: Optional[str] = Form(None),
    contact_no: str = Form(...),
    email: Optional[str] = Form(None),
    logo: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    logo_path = None
    if logo:
        logo_filename = f"{uuid.uuid4()}_{logo.filename}"
        logo_path = os.path.join(LOGO_DIR, logo_filename)
        with open(logo_path, "wb") as f:
            f.write(await logo.read())
        logo_path = f"/static/logos/{logo_filename}"

    update_data = CompanyDetailUpdate(
        company_name=company_name,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        pin=pin,
        state_code=state_code,
        gst_no=gst_no,
        pan_no=pan_no,
        contact_no=contact_no,
        email=email,
        logo_path=logo_path if logo else None,
    )
    company = await get_company_detail(db)
    if company:
        await update_company_detail(db, company.id, update_data)
    else:
        create_data = CompanyDetailCreate(
            company_name=company_name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            pin=pin,
            state_code=state_code,
            gst_no=gst_no,
            pan_no=pan_no,
            contact_no=contact_no,
            email=email,
            logo_path=logo_path,
        )
        await create_company_detail(db, create_data)
    return RedirectResponse("/company", status_code=303)

@company_router.get("/api/lookup_pin")
async def lookup_pin(pin: str):
    try:
        response = requests.get(f"https://api.postalpincode.in/pincode/{pin}")
        data = response.json()
        return data[0]  # Return the first result for simplicity
    except Exception as e:
        logging.error(f"PIN lookup failed: {e}")
        raise HTTPException(status_code=500, detail="PIN lookup failed")

@company_router.get("/api/lookup_gst")
async def lookup_gst(gst: str):
    # Placeholder for GST API (replace with real API if available)
    return {"success": False, "message": "GST API not implemented"}