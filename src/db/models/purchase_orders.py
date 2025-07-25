# src/db/models/purchase_orders.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    po_number = Column(String, unique=True, nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    po_date = Column(String)
    delivery_date = Column(String)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    grn_status = Column(String)
    is_deleted = Column(Integer, default=0)
    payment_terms = Column(String)