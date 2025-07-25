# src/db/crud/crm.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.crm import Lead, Contact, Ticket, FollowUp
from src.db.schemas.crm import LeadCreate, Lead, ContactCreate, Contact, TicketCreate, Ticket, FollowUpCreate, FollowUp
from typing import List

async def create_lead(db: AsyncSession, lead: LeadCreate) -> Lead:
    db_lead = Lead(**lead.dict())
    db.add(db_lead)
    await db.commit()
    await db.refresh(db_lead)
    return db_lead

async def get_leads(db: AsyncSession) -> List[Lead]:
    result = await db.execute(select(Lead))
    return result.scalars().all()

async def create_contact(db: AsyncSession, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def get_contacts(db: AsyncSession) -> List[Contact]:
    result = await db.execute(select(Contact))
    return result.scalars().all()

async def create_ticket(db: AsyncSession, ticket: TicketCreate) -> Ticket:
    db_ticket = Ticket(**ticket.dict())
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def get_tickets(db: AsyncSession) -> List[Ticket]:
    result = await db.execute(select(Ticket))
    return result.scalars().all()

async def create_follow_up(db: AsyncSession, follow_up: FollowUpCreate) -> FollowUp:
    db_follow_up = FollowUp(**follow_up.dict())
    db.add(db_follow_up)
    await db.commit()
    await db.refresh(db_follow_up)
    return db_follow_up

async def get_follow_ups(db: AsyncSession) -> List[FollowUp]:
    result = await db.execute(select(FollowUp))
    return result.scalars().all()