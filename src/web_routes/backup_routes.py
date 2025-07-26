# src/web_routes/backup_routes.py
from fastapi import APIRouter, Request, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.backup import create_backup, perform_restore
from .user_routes import get_current_user

backup_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@backup_router.get("/backup")
async def backup_page(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("backup.html", {"request": request, "current_user": current_user})

@backup_router.post("/backup/create")
async def create_backup_post(db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    path = await create_backup(db)
    return FileResponse(path, media_type="application/octet-stream", filename="erp_backup.sql")

@backup_router.post("/backup/restore")
async def restore_post(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    await perform_restore(db, file)
    return {"message": "Restore completed successfully"}