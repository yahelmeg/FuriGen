from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .auth_utils import *
from .auth_models import Token
import os

router = APIRouter()

@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user= authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expiration_time = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token( data={"sub": user.username}, expires_delta=access_token_expiration_time)
    return Token(access_token=access_token, token_type="bearer")

