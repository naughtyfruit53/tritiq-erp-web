# src/db/models/proforma_invoice_items.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class ProformaInvoiceItem(Base):
    __tablename__ = "proforma_invoice_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    proforma_inv_id = Column(Integer, ForeignKey("proforma_invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)