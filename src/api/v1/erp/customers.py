from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.db import get_db
from src.db.crud.customers import create_customer, get_customers, get_customer, update_customer, delete_customer
from src.db.schemas.customers import CustomerCreate, CustomerInDB, CustomerUpdate
# Assuming you have an auth module; replace with your actual implementation
from src.auth import get_current_user  # Placeholder: Implement this for JWT/OAuth2 auth

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerInDB, status_code=status.HTTP_201_CREATED)
async def create_new_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Auth dependency
):
    return await create_customer(db, customer)

@router.get("/", response_model=List[CustomerInDB])
async def read_customers(
    name: Optional[str] = Query(None, description="Filter by customer name (partial match)"),
    gst_no: Optional[str] = Query(None, description="Filter by GST number"),
    city: Optional[str] = Query(None, description="Filter by city"),
    skip: int = Query(0, ge=0, description="Number of records to skip (pagination offset)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    sort_by: Optional[str] = Query("id", description="Field to sort by (e.g., 'name', 'id')"),
    sort_desc: bool = Query(False, description="Sort in descending order"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Note: Update get_customers in crud to support filters, skip, limit, sort
    # Example: Use SQLAlchemy queries with .filter(Customer.name.ilike(f"%{name}%")) if name, etc.
    # For now, assuming crud.get_customers is updated accordingly
    customers = await get_customers(
        db,
        name=name,
        gst_no=gst_no,
        city=city,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_desc=sort_desc
    )
    return customers

@router.get("/{customer_id}", response_model=CustomerInDB)
async def read_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_customer = await get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=CustomerInDB)
async def update_existing_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_customer = await update_customer(db, customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    deleted = await delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return None  # No content response