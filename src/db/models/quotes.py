# src/db/models/quotes.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    quotation_date = Column(String)
    validity_date = Column(String)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    is_deleted = Column(Integer, default=0)
    payment_terms = Column(String)
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))