# src/db/models/credit_notes.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class CreditNote(Base):
    __tablename__ = "credit_notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cn_number = Column(String, unique=True, nullable=False)
    grn_id = Column(Integer, ForeignKey("grn.id"), nullable=False)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    cn_date = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))