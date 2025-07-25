# src/api/v1/erp/backup.py
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.services.backup import create_backup, perform_restore
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["backup"])

# Assuming templates are in a 'templates' directory at the project root
templates = Jinja2Templates(directory="templates")

@router.get("/backup")
async def backup_page(request: Request):
    return templates.TemplateResponse("backup.html", {"request": request})

@router.post("/backup/create")
async def create_backup_post(db: AsyncSession = Depends(get_db)):
    path = await create_backup(db)
    return FileResponse(path, media_type="application/octet-stream", filename="erp_backup.sql")

@router.post("/restore")
async def restore_post(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    await perform_restore(db, file)
    return {"message": "Restore completed successfully"}