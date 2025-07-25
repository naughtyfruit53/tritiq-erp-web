# src/api/v1/crm/__init__.py
from fastapi import APIRouter

crm_router = APIRouter()

from .leads import router as leads_router
crm_router.include_router(leads_router, prefix="/leads")

from .contacts import router as contacts_router
crm_router.include_router(contacts_router, prefix="/contacts")

from .tickets import router as tickets_router
crm_router.include_router(tickets_router, prefix="/tickets")

from .follow_ups import router as follow_ups_router
crm_router.include_router(follow_ups_router, prefix="/follow_ups")