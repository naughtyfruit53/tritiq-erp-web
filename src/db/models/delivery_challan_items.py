from sqlalchemy import Column, Integer, Float, String, ForeignKey
from .base import Base

class DeliveryChallanItem(Base):
    __tablename__ = "delivery_challan_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dc_id = Column(Integer, ForeignKey("delivery_challans.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    gst_rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)