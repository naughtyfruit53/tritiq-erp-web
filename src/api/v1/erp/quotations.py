from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(tags=["quotations"])

@router.get("/")
async def read_quotations():
    return {"message": "Placeholder for quotations list"}

@router.post("/")
async def create_quotation():
    return {"message": "Placeholder for creating quotation"}

@router.get("/{quotation_id}")
async def read_quotation(quotation_id: int):
    raise HTTPException(status_code=404, detail="Placeholder for quotation details")

@router.put("/{quotation_id}")
async def update_quotation(quotation_id: int):
    raise HTTPException(status_code=404, detail="Placeholder for updating quotation")

@router.delete("/{quotation_id}")
async def delete_quotation(quotation_id: int):
    return {"message": "Placeholder for deleting quotation"}