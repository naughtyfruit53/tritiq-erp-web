# src/db/models/voucher_instances.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class VoucherInstance(Base):
    __tablename__ = "voucher_instances"

    id = Column(Integer, primary_key=True, index=True)
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.id"), nullable=False)
    voucher_number = Column(String, nullable=False)
    data_json = Column(String, nullable=False)  # Stored as JSON string
    module_name = Column(String, nullable=False)
    record_id = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    voucher_type = relationship("VoucherType", back_populates="instances")