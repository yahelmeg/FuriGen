from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
import re

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlmodel import select

from Backend.Database.database import engine
from Backend.User.user_model import User
from .auth_models import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def get_user(username: str):
    session = Session(engine)
    statement = select(User).where(User.username == username)
    user = session.execute(statement).scalars().first()
    return user

def authenticate_user(username: str,password: str):
    user = get_user(username)
    if not user or not verify_password(password,user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    try:
        payload = jwt.decode(token, secret_key, algorithms= [algorithm])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username = username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],):
    if current_user.blocked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Blocked user")
    return current_user

def check_password_strength(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True



