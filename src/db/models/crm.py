# src/db/models/crm.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from .base import Base
from datetime import datetime

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    status = Column(String, default="New")
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    company = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="Open")
    priority = Column(String, default="Medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    contact_id = Column(Integer, ForeignKey("contacts.id"))

class FollowUp(Base):
    __tablename__ = "follow_ups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    description = Column(Text)
    date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)