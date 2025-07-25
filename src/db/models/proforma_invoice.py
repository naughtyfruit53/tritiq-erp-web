# src/db/models/proforma_invoices.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class ProformaInvoice(Base):
    __tablename__ = "proforma_invoices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    proforma_number = Column(String, unique=True, nullable=False)
    quotation_id = Column(Integer, ForeignKey("quotes.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    proforma_date = Column(String)
    validity_date = Column(String)
    total_amount = Column(Float)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    is_deleted = Column(Integer, default=0)
    payment_terms = Column(String)
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))