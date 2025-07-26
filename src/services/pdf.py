# src/services/pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud.sales_orders import get_sales_order
from src.db.crud.sales_invoices import get_sales_invoice
from src.db.crud.purchase_orders import get_purchase_order
from src.db.crud.purchase_inv import get_purchase_inv
from src.db.crud.grn import get_grn
from src.db.crud.rejections import get_rejection  # Assuming this exists; adjust if named differently
from src.db.crud.quotations import get_quotation  # Added for quotation
from src.db.crud.proforma_invoice import get_proforma_invoice  # Added for proforma_invoice
from src.db.crud.credit_notes import get_credit_note  # Added for credit_note
from src.db.crud.delivery_challans import get_delivery_challan  # Added for delivery_challan, assuming CRUD exists

async def generate_sales_order_pdf(sales_order_id: int, db: AsyncSession) -> str:
    data = await get_sales_order(db, sales_order_id)
    path = f"sales_order_{sales_order_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Sales Order ID: {sales_order_id}")
    # Add more data as needed, e.g., loop over items
    c.save()
    return path

async def generate_sales_invoice_pdf(sales_invoice_id: int, db: AsyncSession) -> str:
    data = await get_sales_invoice(db, sales_invoice_id)
    path = f"sales_invoice_{sales_invoice_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Sales Invoice ID: {sales_invoice_id}")
    # Add more data as needed
    c.save()
    return path

async def generate_purchase_order_pdf(purchase_order_id: int, db: AsyncSession) -> str:
    data = await get_purchase_order(db, purchase_order_id)
    path = f"purchase_order_{purchase_order_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Purchase Order ID: {purchase_order_id}")
    # Add more data as needed
    c.save()
    return path

async def generate_purchase_inv_pdf(purchase_inv_id: int, db: AsyncSession) -> str:
    data = await get_purchase_inv(db, purchase_inv_id)
    path = f"purchase_inv_{purchase_inv_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Purchase Invoice ID: {purchase_inv_id}")
    # Add more data as needed
    c.save()
    return path

async def generate_grn_pdf(grn_id: int, db: AsyncSession) -> str:
    data = await get_grn(db, grn_id)
    path = f"grn_{grn_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"GRN ID: {grn_id}")
    # Add more data as needed
    c.save()
    return path

async def generate_rejection_pdf(rejection_id: int, db: AsyncSession) -> str:
    data = await get_rejection(db, rejection_id)  # Assuming get_rejection exists
    path = f"rejection_{rejection_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Rejection ID: {rejection_id}")
    # Add more data as needed
    c.save()
    return path

async def generate_quotation_pdf(quotation_id: int, db: AsyncSession) -> str:
    data = await get_quotation(db, quotation_id)
    path = f"quotation_{quotation_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Quotation ID: {quotation_id}")
    # Add more data as needed, e.g., loop over items
    c.save()
    return path

async def generate_proforma_invoice_pdf(proforma_invoice_id: int, db: AsyncSession) -> str:
    data = await get_proforma_invoice(db, proforma_invoice_id)
    path = f"proforma_invoice_{proforma_invoice_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Proforma Invoice ID: {proforma_invoice_id}")
    # Add more data as needed
    c.save()
    return path

async def generate_credit_note_pdf(credit_note_id: int, db: AsyncSession) -> str:
    data = await get_credit_note(db, credit_note_id)
    path = f"credit_note_{credit_note_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Credit Note ID: {credit_note_id}")
    # Add more data as needed
    c.save()
    return path

async def generate_delivery_challan_pdf(delivery_challan_id: int, db: AsyncSession) -> str:
    data = await get_delivery_challan(db, delivery_challan_id)
    path = f"delivery_challan_{delivery_challan_id}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, f"Delivery Challan ID: {delivery_challan_id}")
    # Add more data as needed
    c.save()
    return path