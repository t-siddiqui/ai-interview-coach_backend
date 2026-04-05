from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from db import users_collection
import os

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey_interview_coach")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid auth credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid auth credentials")

    user = await users_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
