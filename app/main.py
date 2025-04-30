# Entry point

from fastapi import FastAPI, Depends, HTTPException
from app.models import VNetCreateRequest
from app.auth import login_user, get_current_token
from app.azure_client import create_vnet_on_azure
from app.database import load_data
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os

#If the .env is not in the same directory where you run uvicorn, use:
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Azure VNET API!"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)

@app.post("/create-vnet")
async def create_vnet(request: VNetCreateRequest, token: str = Depends(get_current_token)):
    try:
        result = await create_vnet_on_azure(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-vnets")
async def get_vnets(token: str = Depends(get_current_token)):
    try:
        return {"vnets": load_data()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))