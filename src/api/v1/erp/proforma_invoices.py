from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(tags=["proforma_invoices"])

@router.get("/")
async def read_proforma_invoices():
    return {"message": "Placeholder for proforma invoices list"}

@router.post("/")
async def create_proforma_invoice():
    return {"message": "Placeholder for creating proforma invoice"}

@router.get("/{proforma_invoice_id}")
async def read_proforma_invoice(proforma_invoice_id: int):
    raise HTTPException(status_code=404, detail="Placeholder for proforma invoice details")

@router.put("/{proforma_invoice_id}")
async def update_proforma_invoice(proforma_invoice_id: int):
    raise HTTPException(status_code=404, detail="Placeholder for updating proforma invoice")

@router.delete("/{proforma_invoice_id}")
async def delete_proforma_invoice(proforma_invoice_id: int):
    return {"message": "Placeholder for deleting proforma invoice"}