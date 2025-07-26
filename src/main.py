# src/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from src.api.v1 import api_router
from src.web_routes.user_routes import user_router
from src.web_routes.company_routes import company_router
from src.web_routes.product_routes import product_router
from src.web_routes.vendor_routes import vendor_router
from src.web_routes.customer_routes import customer_router
from src.web_routes.voucher_routes import voucher_router
from src.web_routes.sales_routes import sales_router
from src.web_routes.purchase_routes import purchase_router
from src.web_routes.quotation_routes import quotation_router
from src.web_routes.proforma_routes import proforma_router
from src.web_routes.credit_note_routes import credit_note_router
from src.web_routes.pending_routes import pending_router
from src.web_routes.delivery_challan_routes import delivery_challan_router
from src.web_routes.grn_routes import grn_router
from src.web_routes.rejection_routes import rejection_router
from src.web_routes.stock_routes import stock_router
from src.web_routes.manufacturing_routes import manufacturing_router
from src.web_routes.crm_routes import crm_router
from src.web_routes.backup_routes import backup_router
from src.web_routes.custom_voucher_routes import custom_voucher_router
from src.db.session import get_db_context
from src.db.crud.voucher_types import get_voucher_types, create_voucher_type
from src.db.crud.voucher_instances import get_voucher_instance_counts_by_types
from src.db.schemas.voucher_types import VoucherTypeCreate
import logging

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.include_router(user_router)
app.include_router(company_router)
app.include_router(product_router)
app.include_router(vendor_router)
app.include_router(customer_router)
app.include_router(voucher_router)
app.include_router(sales_router)
app.include_router(purchase_router)
app.include_router(quotation_router)
app.include_router(proforma_router)
app.include_router(credit_note_router)
app.include_router(pending_router)
app.include_router(delivery_challan_router)
app.include_router(grn_router)
app.include_router(rejection_router)
app.include_router(stock_router)
app.include_router(manufacturing_router)
app.include_router(crm_router)
app.include_router(backup_router)
app.include_router(custom_voucher_router)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

logging.basicConfig(filename='logs/erp_app.log', level=logging.DEBUG)

async def seed_voucher_types(db):
    """Seed initial voucher types if none exist."""
    existing = await get_voucher_types(db)
    if not existing:
        predefined = [
            VoucherTypeCreate(name="Sales Order", module_name="sales_order", category="sales", is_default=True),
            VoucherTypeCreate(name="Sales Invoice", module_name="sales_inv", category="sales", is_default=False),
            VoucherTypeCreate(name="Purchase Order", module_name="purchase_order", category="purchase", is_default=False),
            VoucherTypeCreate(name="Purchase Invoice", module_name="purchase_inv", category="purchase", is_default=False),
            VoucherTypeCreate(name="Quotation", module_name="quotation", category="sales", is_default=False),
            VoucherTypeCreate(name="Proforma Invoice", module_name="proforma_invoice", category="sales", is_default=False),
            VoucherTypeCreate(name="Credit Note", module_name="credit_note", category="financial", is_default=False),
            VoucherTypeCreate(name="GRN", module_name="grn", category="purchase", is_default=False),
            VoucherTypeCreate(name="Rejection", module_name="rejection", category="purchase", is_default=False),
            VoucherTypeCreate(name="Delivery Challan", module_name="delivery_challan", category="sales", is_default=False),
        ]
        for vt in predefined:
            await create_voucher_type(db, vt)
        logging.info("Seeded initial voucher types.")

@app.on_event("startup")
async def startup_event():
    async with get_db_context() as db:
        await seed_voucher_types(db)

@app.middleware("http")
async def add_voucher_categories(request: Request, call_next):
    try:
        async with get_db_context() as db:
            voucher_types = await get_voucher_types(db)
            
            # Get instance counts for all voucher types efficiently
            voucher_type_ids = [vt.id for vt in voucher_types]
            instance_counts = await get_voucher_instance_counts_by_types(db, voucher_type_ids) if voucher_type_ids else {}
            
            # Route mappings for predefined voucher types
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
            
            # Initialize category groups
            purchase = []
            sales = []
            financial = []
            internal = []
            
            for vt in voucher_types:
                # Get instance count for this voucher type
                count = instance_counts.get(vt.id, 0)
                
                # Get the appropriate link
                vt_link = mappings.get(vt.module_name, f"/voucher_instances?type_id={vt.id}")
                
                # Create voucher dict with instance count
                vt_dict = {
                    "name": vt.name if hasattr(vt, 'name') else vt.module_name.replace('_', ' ').title(),
                    "link": vt_link,
                    "id": vt.id,
                    "count": count,
                    "create_link": mappings.get(vt.module_name + "_create", f"/voucher_instances/create?type_id={vt.id}")
                }
                
                # Group by category
                category = getattr(vt, 'category', 'internal')
                if category == 'purchase':
                    purchase.append(vt_dict)
                elif category == 'sales':
                    sales.append(vt_dict)
                elif category == 'financial':
                    financial.append(vt_dict)
                else:
                    internal.append(vt_dict)
            
            # Calculate category totals
            grouped = {
                "purchase": purchase, 
                "sales": sales, 
                "financial": financial, 
                "internal": internal,
                "totals": {
                    "purchase": sum(v["count"] for v in purchase),
                    "sales": sum(v["count"] for v in sales),
                    "financial": sum(v["count"] for v in financial),
                    "internal": sum(v["count"] for v in internal)
                }
            }
            request.state.grouped_vouchers = grouped
    except Exception as e:
        logging.error(f"Failed to load voucher categories: {e}")
        request.state.grouped_vouchers = {
            "purchase": [], "sales": [], "financial": [], "internal": [],
            "totals": {"purchase": 0, "sales": 0, "financial": 0, "internal": 0}
        }
    response = await call_next(request)
    return response