# src/db/models/po_items.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class PoItem(Base):
    __tablename__ = "po_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)