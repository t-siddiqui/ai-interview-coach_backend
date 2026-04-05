import random
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db import users_collection
from utils.auth_utils import get_password_hash, verify_password, create_access_token

router = APIRouter()

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str

@router.post("/register")
async def register(user: UserRegister):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    }
    await users_collection.insert_one(user_dict)
    
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user:
         raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user["password"]):
         raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "name": db_user["name"], "email": db_user["email"]}

# Placeholder for OAuth
@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest):
    user = await users_collection.find_one({"email": req.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = str(random.randint(100000, 999999))
    otp_expires = datetime.utcnow() + timedelta(minutes=15)
    
    await users_collection.update_one(
        {"email": req.email},
        {"$set": {"reset_otp": otp, "reset_otp_expires": otp_expires}}
    )
    
    return {"message": "OTP generated successfully", "otp": otp}

@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest):
    user = await users_collection.find_one({"email": req.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if "reset_otp" not in user or user["reset_otp"] != req.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
        
    if "reset_otp_expires" in user and datetime.utcnow() > user["reset_otp_expires"]:
        raise HTTPException(status_code=400, detail="OTP expired")
        
    hashed_password = get_password_hash(req.new_password)
    
    await users_collection.update_one(
        {"email": req.email},
        {
            "$set": {"password": hashed_password},
            "$unset": {"reset_otp": "", "reset_otp_expires": ""}
        }
    )
    
    return {"message": "Password reset successful"}

@router.get("/oauth/{provider}")
async def oauth_login(provider: str):
    # In a real app, this redirects to Google/Github/Linkedin OAuth page
    # and handles callbacks. For now, since no keys are available, we simulate.
    return {"message": f"OAuth for {provider} not configured with real Secret Keys yet."}

