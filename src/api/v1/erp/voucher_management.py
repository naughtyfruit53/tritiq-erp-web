import logging
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import get_log_path
from ....db import get_db
from ....db.crud.voucher_types import (
    create_voucher_type as create_voucher_type_db,
    get_voucher_types,
    get_voucher_type_by_name,
    update_voucher_type,
    delete_voucher_type
)
from ....db.crud.voucher_columns import (
    create_voucher_column,
    get_voucher_columns,
    get_voucher_column,
    update_voucher_column,
    delete_voucher_column
)
from ....db.crud.voucher_instances import (
    create_voucher_instance,
    get_voucher_instances_by_type
)
from ....db.schemas.voucher_types import VoucherTypeCreate, VoucherTypeInDB
from ....db.schemas.voucher_columns import VoucherColumnCreate, VoucherColumnUpdate
from ....db.schemas.voucher_instances import VoucherInstanceCreate, VoucherInstance
from ..services.sequence import get_next_voucher_number
from ....services.utils import VOUCHER_COLUMNS

logging.basicConfig(filename=get_log_path(), level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/vouchers", tags=["vouchers"])
templates = Jinja2Templates(directory="templates")

VOUCHER_CATEGORIES = {
    "inward": {
        "Purchase Order": {"module": "purchase_order", "view_path": "/erp/purchase_orders", "create_path": "/erp/purchase_orders/create"},
        "GRN": {"module": "grn", "view_path": "/erp/grn", "create_path": "/erp/grn/create"},
        "Purchase Invoice": {"module": "purchase_inv", "view_path": "/erp/purchase_inv", "create_path": "/erp/purchase_inv/create"},
        "Debit Note": {"module": "debit_note", "view_path": "/erp/debit_notes", "create_path": "/erp/debit_notes/create"}
    },
    "outward": {
        "Quotation": {"module": "quotation", "view_path": "/erp/quotations", "create_path": "/erp/quotations/create"},
        "Sales Order": {"module": "sales_order", "view_path": "/erp/sales_orders", "create_path": "/erp/sales_orders/create"},
        "Proforma Invoice": {"module": "proforma_invoice", "view_path": "/erp/proforma_invoices", "create_path": "/erp/proforma_invoices/create"},
        "Delivery Challan": {"module": "delivery_challan", "view_path": "/erp/delivery_challan", "create_path": "/erp/delivery_challan/create"},
        "Sales Invoice": {"module": "sales_inv", "view_path": "/erp/sales_invoices", "create_path": "/erp/sales_invoices/create"},
        "Credit Note": {"module": "credit_note", "view_path": "/erp/credit_notes", "create_path": "/erp/credit_notes/create"}
    }
}

COLUMN_DATA_TYPES = {
    "Voucher Number": "TEXT", "Voucher Date": "DATE", "Due Date": "DATE", "Reference Number": "TEXT",
    "Party Name": "TEXT", "Ledger Account": "TEXT", "Item Description": "TEXT", "Item Code": "TEXT",
    "HSN/SAC Code": "TEXT", "Quantity": "INTEGER", "Unit of Measure": "TEXT", "Unit Price": "REAL",
    "Total Amount": "REAL", "Discount Percentage": "REAL", "Discount Amount": "REAL", "Tax Rate": "REAL",
    "Tax Amount": "REAL", "CGST Amount": "REAL", "SGST Amount": "REAL", "IGST Amount": "REAL",
    "Cess Amount": "REAL", "GSTIN": "TEXT", "Narration": "TEXT", "Payment Terms": "TEXT",
    "Shipping Address": "TEXT", "Billing Address": "TEXT", "Place of Supply": "TEXT",
    "Terms and Conditions": "TEXT", "Round Off": "REAL", "Net Amount": "REAL", "Freight Charges": "REAL",
    "Packing Charges": "REAL", "Insurance Charges": "REAL", "Batch Number": "TEXT", "Expiry Date": "DATE",
    "Serial Number": "TEXT", "Warranty Period": "TEXT", "E-Way Bill Number": "TEXT", "Transport Mode": "TEXT",
    "Vehicle Number": "TEXT", "LR/RR Number": "TEXT", "PO Number": "TEXT", "GRN Number": "TEXT",
    "Invoice Number": "TEXT", "Credit Period": "TEXT", "TDS Amount": "REAL", "TCS Amount": "REAL",
    "Cost Center": "TEXT", "Project Code": "TEXT", "Currency": "TEXT", "Exchange Rate": "REAL",
    "Bank Details": "TEXT", "Reverse Charge": "TEXT", "Export Type": "TEXT", "Port Code": "TEXT",
    "Shipping Bill Number": "TEXT", "Country of Origin": "TEXT"
}

@router.get("/{category}/view", response_class=HTMLResponse)
async def view_vouchers(category: str, request: Request, db: AsyncSession = Depends(get_db)):
    if category not in VOUCHER_CATEGORIES:
        raise HTTPException(404, "Invalid category")
    module_names = [info["module"] for info in VOUCHER_CATEGORIES[category].values()]
    all_voucher_types = await get_voucher_types(db)
    voucher_types_list = [vt for vt in all_voucher_types if vt.module_name in module_names]
    voucher_types_list.append(VoucherTypeInDB(name="Custom Voucher", module_name="", is_default=False, id=0))  # Dummy
    logger.debug(f"Viewing vouchers for {category}: {[vt.name for vt in voucher_types_list]}")
    return templates.TemplateResponse("erp/voucher_management.html", {
        "request": request, "category": category, "mode": "view", "voucher_types": voucher_types_list
    })

@router.get("/{category}/create", response_class=HTMLResponse)
async def create_voucher(category: str, request: Request, db: AsyncSession = Depends(get_db)):
    if category not in VOUCHER_CATEGORIES:
        raise HTTPException(404, "Invalid category")
    module_names = [info["module"] for info in VOUCHER_CATEGORIES[category].values()]
    all_voucher_types = await get_voucher_types(db)
    voucher_types_list = [vt for vt in all_voucher_types if vt.module_name in module_names]
    voucher_types_list.append(VoucherTypeInDB(name="Custom Voucher", module_name="", is_default=False, id=0))
    return templates.TemplateResponse("erp/voucher_management.html", {
        "request": request, "category": category, "mode": "create", "voucher_types": voucher_types_list
    })

@router.get("/content/{voucher_type_name}", response_class=HTMLResponse)
async def get_voucher_content(voucher_type_name: str, mode: str, category: str, request: Request, db: AsyncSession = Depends(get_db)):
    if voucher_type_name == "Custom Voucher":
        return templates.TemplateResponse("erp/custom_voucher_form.html", {"request": request})
    
    voucher_type = await get_voucher_type_by_name(db, voucher_type_name)
    if not voucher_type:
        raise HTTPException(404, "Voucher type not found")
    
    voucher_info = VOUCHER_CATEGORIES.get(category, {}).get(voucher_type_name)
    if voucher_info:
        path = voucher_info["view_path"] if mode == "view" else voucher_info["create_path"]
        return RedirectResponse(url=path)
    
    # Generic handling
    columns = await get_voucher_columns(db, voucher_type.id)
    if mode == "view":
        instances = await get_voucher_instances_by_type(db, voucher_type.id)
        parsed_instances = [{**inst.model_dump(), 'data_json': json.loads(inst.data_json)} for inst in instances]
        return templates.TemplateResponse("erp/voucher_index.html", {"request": request, "columns": columns, "instances": parsed_instances})
    else:
        return templates.TemplateResponse("erp/voucher_form.html", {"request": request, "columns": columns, "voucher_type_id": voucher_type.id})

@router.post("/instances")
async def save_voucher_instance(voucher_type_id: int = Form(...), data_json: str = Form(...), module_name: str = Form(...), db: AsyncSession = Depends(get_db)):
    try:
        voucher_number = await get_next_voucher_number(db, voucher_type_id)
        create_data = VoucherInstanceCreate(voucher_type_id=voucher_type_id, voucher_number=voucher_number, data_json=json.loads(data_json), module_name=module_name)
        instance = await create_voucher_instance(db, create_data)
        return {"success": True, "voucher_number": voucher_number, "instance_id": instance.id}
    except Exception as e:
        logger.error(f"Error saving voucher: {e}")
        raise HTTPException(500, "Failed to save voucher")

@router.post("/types")
async def create_custom_voucher_type(name: str = Form(...), module_name: str = Form(...), db: AsyncSession = Depends(get_db)):
    vt_create = VoucherTypeCreate(name=name, is_default=False, module_name=module_name)
    vt = await create_voucher_type_db(db, vt_create)
    return {"success": True, "voucher_type_id": vt.id}

@router.post("/columns")
async def add_voucher_column(voucher_type_id: int = Form(...), column_name: str = Form(...), is_mandatory: bool = Form(False), display_order: int = Form(1), db: AsyncSession = Depends(get_db)):
    data_type = COLUMN_DATA_TYPES.get(column_name, "TEXT")
    col_create = VoucherColumnCreate(voucher_type_id=voucher_type_id, column_name=column_name, data_type=data_type, is_mandatory=is_mandatory, display_order=display_order)
    col = await create_voucher_column(db, col_create)
    return {"success": True, "column_id": col.id}

@router.delete("/columns/{column_id}")
async def delete_voucher_column(column_id: int, db: AsyncSession = Depends(get_db)):
    await delete_voucher_column(db, column_id)
    return {"success": True}

# Placeholder for Debit Note
@router.get("/debit_notes")
async def debit_note_index():
    return {"message": "Debit Note Index - Coming Soon"}

@router.post("/debit_notes/create")
async def debit_note_form():
    return {"message": "Debit Note Form - Coming Soon"}