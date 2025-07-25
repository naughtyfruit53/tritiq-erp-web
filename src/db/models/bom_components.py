from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class BOMComponent(Base):
    __tablename__ = "bom_components"
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("bom.id"), nullable=False)
    component_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)