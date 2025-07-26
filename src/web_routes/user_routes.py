# src/web_routes/user_routes.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict  # Added import for Dict
from src.db import get_db
from src.db.crud.users import get_users, create_user, get_user_by_username
from src.db.schemas.users import UserCreate
import bcrypt
import uuid

user_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

sessions: Dict[str, str] = {}  # session_id: username

def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        return sessions[session_id]
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

@user_router.get("/")
async def root(request: Request, db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    if not users:
        return RedirectResponse("/setup")
    return templates.TemplateResponse("login.html", {"request": request})

@user_router.get("/home")
async def home_page(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request, "current_user": current_user})

@user_router.get("/setup")
async def setup_page(request: Request, db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    if users:
        return RedirectResponse("/")
    return templates.TemplateResponse("setup.html", {"request": request})  # Add setup.html with form POST to /setup

@user_router.post("/setup")
async def create_first_user(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    users = await get_users(db)
    if users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Setup already completed")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_create = UserCreate(username=username, password=hashed_password, role="admin", active=True, must_change_password=True)
    await create_user(db, user_create)
    return RedirectResponse("/", status_code=303)

@user_router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_username(db, username)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Create simple session
    session_id = str(uuid.uuid4())
    sessions[session_id] = username
    response = RedirectResponse("/home", status_code=303)  # Changed to /home
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

@user_router.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        sessions.pop(session_id, None)
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session_id")
    return response

@user_router.get("/dashboard")
async def dashboard(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "current_user": current_user})

@user_router.get("/users")
async def users_page(request: Request, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    users = await get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "current_user": current_user})