# src/api/v1/services/auth.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.db.crud.users import get_user_by_username, update_user
from src.db.schemas.users import UserUpdate
import bcrypt
from jose import JWTError, jwt  # pip install pyjwt for JWT support
from datetime import datetime, timedelta
from typing import Optional

# Secret key for JWT (change this to a secure random key in production)
SECRET_KEY = "your_super_secret_key_here_change_me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def authenticate_user(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def change_password(username: str, old_password: str, new_password: str, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(username, old_password, db)  # Verifies old password
    hashed_new_password = hash_password(new_password)
    user_update = UserUpdate(password=hashed_new_password, must_change_password=False)
    await update_user(db, user.id, user_update)
    return {"message": "Password changed successfully"}

# Optional JWT utils (use instead of sessions if preferred)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_from_token(token: str, db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

# Example usage in a route (add to main.py if using JWT):
# @app.post("/token")
# async def login_for_access_token(username: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
#     user = await authenticate_user(username, password, db)
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}