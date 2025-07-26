# src/db/models/quotations.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from datetime import datetime
from .base import Base

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String, unique=True, nullable=False)
    quotation_date = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))
    voucher_data = Column(String)