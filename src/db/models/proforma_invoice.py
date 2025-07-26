# src/db/models/proforma_invoice.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base
from datetime import datetime

class ProformaInvoice(Base):
    __tablename__ = "proforma_invoices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    proforma_inv_number = Column(String, unique=True, nullable=False)
    proforma_date = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))
    voucher_data = Column(String)