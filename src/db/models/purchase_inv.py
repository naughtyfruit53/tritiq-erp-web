# src/db/models/purchase_inv.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class PurchaseInv(Base):
    __tablename__ = "purchase_inv"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pur_inv_number = Column(String, unique=True, nullable=False)
    invoice_number = Column(String)
    invoice_date = Column(String)
    grn_id = Column(Integer, ForeignKey("grn.id"), nullable=False)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    pur_inv_date = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    cgst_amount = Column(Float)
    sgst_amount = Column(Float)
    igst_amount = Column(Float)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"))