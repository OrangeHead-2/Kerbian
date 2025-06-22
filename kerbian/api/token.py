from fastapi import APIRouter, Form
from kerbian.auth.jwt_auth import create_access_token

router = APIRouter()

@router.post("/token")
async def login(username: str = Form(...), password: str = Form(...)):
    # Replace with real user lookup & password check
    if username == "admin" and password == "password":
        return {"access_token": create_access_token({"sub": 1, "role": "admin"}), "token_type": "bearer"}
    return {"error": "Invalid credentials"}