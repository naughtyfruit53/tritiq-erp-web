# src/db/models/voucher_types.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class VoucherType(Base):
    __tablename__ = "voucher_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    module_name = Column(String, nullable=False)
    category = Column(String, nullable=False, default="internal")
    
    # Add the missing back_populates relationship to VoucherInstance
    instances = relationship("VoucherInstance", back_populates="voucher_type")
    
    def __repr__(self):
        return f"<VoucherType(id={self.id}, name='{self.name}', is_default={self.is_default})>"