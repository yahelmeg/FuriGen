from sqlalchemy.orm import Session
from sqlmodel import select
from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/user")