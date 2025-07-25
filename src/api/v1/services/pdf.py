from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tempfile import NamedTemporaryFile
from src.db import get_db
from src.db.crud.sales_orders import get_sales_order
from src.db.crud.sales_invoices import get_sales_invoice
from src.db.crud.purchase_orders import get_purchase_order
from src.db.crud.purchase_inv import get_purchase_inv
from sqlalchemy.ext.asyncio import AsyncSession

async def generate_sales_order_pdf(sales_order_id: int, db: AsyncSession) -> str:
    sales_order = await get_sales_order(db, sales_order_id)
    if not sales_order:
        raise ValueError("Sales Order not found")
    with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        c = canvas.Canvas(tmp.name, pagesize=letter)
        c.drawString(100, 750, f"Sales Order {sales_order.sales_order_number}")
        c.drawString(100, 730, f"Customer ID: {sales_order.customer_id}")
        c.drawString(100, 710, f"Date: {sales_order.sales_order_date}")
        c.drawString(100, 690, f"Delivery Date: {sales_order.delivery_date or 'N/A'}")
        c.drawString(100, 670, f"Payment Terms: {sales_order.payment_terms or 'N/A'}")
        y = 650
        c.drawString(100, y, "Items:")
        y -= 20
        for item in sales_order.items:
            c.drawString(100, y, f"{item.product_name}: {item.quantity} {item.unit} @ {item.unit_price} (GST: {item.gst_rate}%) = {item.amount}")
            y -= 20
        c.drawString(100, y, f"Total: {sales_order.total_amount}")
        c.drawString(100, y-20, f"CGST: {sales_order.cgst_amount or 0}")
        c.drawString(100, y-40, f"SGST: {sales_order.sgst_amount or 0}")
        c.drawString(100, y-60, f"IGST: {sales_order.igst_amount or 0}")
        c.save()
    return tmp.name

async def generate_sales_invoice_pdf(sales_invoice_id: int, db: AsyncSession) -> str:
    sales_invoice = await get_sales_invoice(db, sales_invoice_id)
    if not sales_invoice:
        raise ValueError("Sales Invoice not found")
    with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        c = canvas.Canvas(tmp.name, pagesize=letter)
        c.drawString(100, 750, f"Sales Invoice {sales_invoice.sales_inv_number}")
        c.drawString(100, 730, f"Customer ID: {sales_invoice.customer_id}")
        c.drawString(100, 710, f"Invoice Date: {sales_invoice.invoice_date}")
        c.drawString(100, 690, f"Sales Order ID: {sales_invoice.sales_order_id or 'N/A'}")
        y = 670
        c.drawString(100, y, "Items:")
        y -= 20
        for item in sales_invoice.items:
            c.drawString(100, y, f"Product ID {item.product_id}: {item.quantity} {item.unit} @ {item.unit_price} (GST: {item.gst_rate}%) = {item.amount}")
            y -= 20
        c.drawString(100, y, f"Total: {sales_invoice.total_amount}")
        c.drawString(100, y-20, f"CGST: {sales_invoice.cgst_amount or 0}")
        c.drawString(100, y-40, f"SGST: {sales_invoice.sgst_amount or 0}")
        c.drawString(100, y-60, f"IGST: {sales_invoice.igst_amount or 0}")
        c.save()
    return tmp.name

async def generate_purchase_order_pdf(purchase_order_id: int, db: AsyncSession) -> str:
    purchase_order = await get_purchase_order(db, purchase_order_id)
    if not purchase_order:
        raise ValueError("Purchase Order not found")
    with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        c = canvas.Canvas(tmp.name, pagesize=letter)
        c.drawString(100, 750, f"Purchase Order {purchase_order.po_number}")
        c.drawString(100, 730, f"Vendor ID: {purchase_order.vendor_id}")
        c.drawString(100, 710, f"PO Date: {purchase_order.po_date}")
        c.drawString(100, 690, f"Delivery Date: {purchase_order.delivery_date or 'N/A'}")
        c.drawString(100, 670, f"Payment Terms: {purchase_order.payment_terms or 'N/A'}")
        y = 650
        c.drawString(100, y, "Items:")
        y -= 20
        for item in purchase_order.items:
            c.drawString(100, y, f"Product ID {item.product_id}: {item.quantity} {item.unit} @ {item.unit_price} (GST: {item.gst_rate}%) = {item.amount}")
            y -= 20
        c.drawString(100, y, f"Total: {purchase_order.total_amount}")
        c.drawString(100, y-20, f"CGST: {purchase_order.cgst_amount or 0}")
        c.drawString(100, y-40, f"SGST: {purchase_order.sgst_amount or 0}")
        c.drawString(100, y-60, f"IGST: {purchase_order.igst_amount or 0}")
        c.save()
    return tmp.name

async def generate_purchase_inv_pdf(purchase_inv_id: int, db: AsyncSession) -> str:
    purchase_inv = await get_purchase_inv(db, purchase_inv_id)
    if not purchase_inv:
        raise ValueError("Purchase Invoice not found")
    with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        c = canvas.Canvas(tmp.name, pagesize=letter)
        c.drawString(100, 750, f"Purchase Invoice {purchase_inv.pur_inv_number}")
        c.drawString(100, 730, f"Vendor ID: {purchase_inv.vendor_id}")
        c.drawString(100, 710, f"Invoice Number: {purchase_inv.invoice_number}")
        c.drawString(100, 690, f"Invoice Date: {purchase_inv.invoice_date}")
        c.drawString(100, 670, f"PO ID: {purchase_inv.po_id}")
        y = 650
        c.drawString(100, y, "Items:")
        y -= 20
        for item in purchase_inv.items:
            c.drawString(100, y, f"Product ID {item.product_id}: {item.quantity} {item.unit} @ {item.unit_price} (GST: {item.gst_rate}%) = {item.amount}")
            y -= 20
        c.drawString(100, y, f"Total: {purchase_inv.total_amount}")
        c.drawString(100, y-20, f"CGST: {purchase_inv.cgst_amount or 0}")
        c.drawString(100, y-40, f"SGST: {purchase_inv.sgst_amount or 0}")
        c.drawString(100, y-60, f"IGST: {purchase_inv.igst_amount or 0}")
        c.save()
    return tmp.name