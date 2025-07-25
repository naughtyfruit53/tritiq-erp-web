from sqlalchemy import Column, Integer, Float, String, ForeignKey
from .base import Base

class GrnItem(Base):
    __tablename__ = "grn_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    grn_id = Column(Integer, ForeignKey("grn.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    po_item_id = Column(Integer, ForeignKey("po_items.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    accepted_quantity = Column(Float, nullable=False)
    rejected_quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    remarks = Column(String)