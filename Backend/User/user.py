from sqlalchemy.orm import Session
from .user_model import User, UserCreateRequest
from fastapi import APIRouter, status, HTTPException
from Backend.Auth.auth_utils import hash_password, check_password_strength
from Backend.Database.database import engine
from sqlmodel import select

router = APIRouter(prefix="/user")

@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateRequest):
    session = Session(engine)
    statement = select(User).where(User.username == user.username)
    existing_user = session.execute(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )

    if not check_password_strength(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password isn't strong enough"
        )
    new_user = User(username=user.username, hashed_password= hash_password(user.password), blocked= False)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}
