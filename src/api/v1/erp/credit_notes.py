# src/api/v1/erp/credit_notes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.credit_notes import create_credit_note, get_credit_notes, get_credit_note, update_credit_note, delete_credit_note
from src.db.schemas.credit_notes import CreditNoteCreate, CreditNoteInDB, CreditNoteUpdate

router = APIRouter(tags=["credit_notes"])

@router.post("/", response_model=CreditNoteInDB)
async def create_new_credit_note(credit_note: CreditNoteCreate, db: AsyncSession = Depends(get_db)):
    return await create_credit_note(db, credit_note)

@router.get("/", response_model=List[CreditNoteInDB])
async def read_credit_notes(db: AsyncSession = Depends(get_db)):
    return await get_credit_notes(db)

@router.get("/{credit_note_id}", response_model=CreditNoteInDB)
async def read_credit_note(credit_note_id: int, db: AsyncSession = Depends(get_db)):
    db_credit_note = await get_credit_note(db, credit_note_id)
    if db_credit_note is None:
        raise HTTPException(status_code=404, detail="Credit Note not found")
    return db_credit_note

@router.put("/{credit_note_id}", response_model=CreditNoteInDB)
async def update_existing_credit_note(credit_note_id: int, credit_note: CreditNoteUpdate, db: AsyncSession = Depends(get_db)):
    db_credit_note = await update_credit_note(db, credit_note_id, credit_note)
    if db_credit_note is None:
        raise HTTPException(status_code=404, detail="Credit Note not found")
    return db_credit_note

@router.delete("/{credit_note_id}")
async def delete_existing_credit_note(credit_note_id: int, db: AsyncSession = Depends(get_db)):
    await delete_credit_note(db, credit_note_id)
    return {"detail": "Credit Note deleted"}