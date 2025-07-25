# src/db/models/proforma_invoice_items.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class ProformaInvoiceItem(Base):
    __tablename__ = "proforma_invoice_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    proforma_id = Column(Integer, ForeignKey("proforma_invoices.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    unit = Column(String)
    unit_price = Column(Float)
    gst_rate = Column(Float)
    amount = Column(Float)