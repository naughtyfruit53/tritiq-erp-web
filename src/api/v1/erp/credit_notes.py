from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(tags=["credit_notes"])

@router.get("/")
async def read_credit_notes():
    return {"message": "Placeholder for credit notes list"}

@router.post("/")
async def create_credit_note():
    return {"message": "Placeholder for creating credit note"}

@router.get("/{credit_note_id}")
async def read_credit_note(credit_note_id: int):
    raise HTTPException(status_code=404, detail="Placeholder for credit note details")

@router.put("/{credit_note_id}")
async def update_credit_note(credit_note_id: int):
    raise HTTPException(status_code=404, detail="Placeholder for updating credit note")

@router.delete("/{credit_note_id}")
async def delete_credit_note(credit_note_id: int):
    return {"message": "Placeholder for deleting credit note"}