# Authentication logic

from dotenv import load_dotenv
import os

load_dotenv()  # Automatically loads from .env in current working dir

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(username: str, password: str):
    return username == "admin" and password == "password"

def get_current_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    if authenticate_user(form_data.username, form_data.password):
        return {"access_token": str(uuid.uuid4()), "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )