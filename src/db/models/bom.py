from sqlalchemy import Column, Integer, ForeignKey, DateTime
from .base import Base  # Import Base from your base model file

class BOM(Base):
    __tablename__ = "bom"
    id = Column(Integer, primary_key=True, index=True)
    manufactured_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)