from sqlalchemy import Column, Integer, Float, String, ForeignKey
from .base import Base

class Rejection(Base):
    __tablename__ = "rejections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    grn_id = Column(Integer, ForeignKey("grn.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    reason = Column(String, nullable=False)
    date = Column(String, nullable=False)