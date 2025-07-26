# src/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from src.api.v1 import api_router
from src.web_routes import web_router
from src.db import get_db
from src.db.crud.voucher_types import get_voucher_types
import logging

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.include_router(web_router)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

logging.basicConfig(filename='logs/erp_app.log', level=logging.DEBUG)

@app.middleware("http")
async def add_voucher_categories(request: Request, call_next):
    try:
        async with get_db() as db:
            voucher_types = await get_voucher_types(db)
            mappings = {
                "sales_order": "/sales_orders",
                "sales_inv": "/sales_invoices",
                "purchase_order": "/purchase_orders",
                "purchase_inv": "/purchase_invoices",
                "quotation": "/quotations",
                "proforma_invoice": "/proforma_invoices",
                "credit_note": "/credit_notes",
                "grn": "/grn",
                "rejection": "/rejections",
                "delivery_challan": "/delivery_challan",
            }
            purchase = []
            sales = []
            financial = []
            internal = []
            for vt in voucher_types:
                vt_link = mappings.get(vt.module_name, "/voucher_types")
                vt_dict = {"name": vt.name if hasattr(vt, 'name') else vt.module_name.replace('_', ' ').capitalize(), "link": vt_link, "id": vt.id}
                if vt.category == 'purchase':
                    purchase.append(vt_dict)
                elif vt.category == 'sales':
                    sales.append(vt_dict)
                elif vt.category == 'financial':
                    financial.append(vt_dict)
                elif vt.category == 'internal':
                    internal.append(vt_dict)
            grouped = {"purchase": purchase, "sales": sales, "financial": financial, "internal": internal}
            request.state.grouped_vouchers = grouped
    except Exception as e:
        logging.error(f"Failed to load voucher categories: {e}")
        request.state.grouped_vouchers = {"purchase": [], "sales": [], "financial": [], "internal": []}
    response = await call_next(request)
    return response