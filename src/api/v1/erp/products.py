# src/api/v1/erp/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db import get_db
from src.db.crud.products import create_product, get_products, get_product, update_product, delete_product
from src.db.schemas.products import ProductCreate, ProductInDB, ProductUpdate

router = APIRouter()

@router.post("/", response_model=ProductInDB)
async def create_new_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, product)

@router.get("/", response_model=List[ProductInDB])
async def read_products(db: AsyncSession = Depends(get_db)):
    return await get_products(db)

@router.get("/{product_id}", response_model=ProductInDB)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductInDB)
async def update_existing_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    db_product = await update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
async def delete_existing_product(product_id: int, db: AsyncSession = Depends(get_db)):
    await delete_product(db, product_id)
    return {"detail": "Product deleted"}