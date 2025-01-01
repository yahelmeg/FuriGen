from Backend.User.user_model import User
from sqlalchemy.orm import Session
from Backend.Database.database import  engine
from sqlmodel import select
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hashed_password: str):
    pwd_context.verify(password, hashed_password)

def get_password_hash(password: str):
    pwd_context.hash(password)

def authenticate_user(username: str,password: str):
    session = Session(engine)
    statement = select(User).where(User.id == username)
    user = session.execute(statement).scalars().first()
    if not user or not verify_password(password,user.hashed_password):
        return None
    return user


