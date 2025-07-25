from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.material_transactions import create_material_transaction, get_material_transactions, get_material_transaction, update_material_transaction, delete_material_transaction
from src.db.schemas.material_transactions import MaterialTransactionCreate, MaterialTransactionInDB, MaterialTransactionUpdate

router = APIRouter(tags=["material_transactions"])

@router.post("/", response_model=MaterialTransactionInDB)
async def create_new_material_transaction(material_transaction: MaterialTransactionCreate, db: AsyncSession = Depends(get_db)):
    return await create_material_transaction(db, material_transaction)

@router.get("/", response_model=List[MaterialTransactionInDB])
async def read_material_transactions(db: AsyncSession = Depends(get_db)):
    return await get_material_transactions(db)

@router.get("/{material_transaction_id}", response_model=MaterialTransactionInDB)
async def read_material_transaction(material_transaction_id: int, db: AsyncSession = Depends(get_db)):
    db_material_transaction = await get_material_transaction(db, material_transaction_id)
    if db_material_transaction is None:
        raise HTTPException(status_code=404, detail="Material Transaction not found")
    return db_material_transaction

@router.put("/{material_transaction_id}", response_model=MaterialTransactionInDB)
async def update_existing_material_transaction(material_transaction_id: int, material_transaction: MaterialTransactionUpdate, db: AsyncSession = Depends(get_db)):
    db_material_transaction = await update_material_transaction(db, material_transaction_id, material_transaction)
    if db_material_transaction is None:
        raise HTTPException(status_code=404, detail="Material Transaction not found")
    return db_material_transaction

@router.delete("/{material_transaction_id}")
async def delete_existing_material_transaction(material_transaction_id: int, db: AsyncSession = Depends(get_db)):
    await delete_material_transaction(db, material_transaction_id)
    return {"detail": "Material Transaction deleted"}