import json
from fastapi import APIRouter, Request, Response, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from typing import Annotated
from datetime import timedelta, datetime, timezone

from backend.utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS, verify_password, oauth2_scheme
from backend.database import user_collection
from backend.models import Token, TokenData


router = APIRouter(prefix="/token", tags=["Auth"])


async def authenticate_user(username: str, password: str):
    user = await user_collection.find_one({"email": username})
    if not user:
        return False
    db_password = user["password"]
    if not verify_password(password, db_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(username: str):
    user = await user_collection.find_one({"email": username})
    if user:
        return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user["password"]}, expires_delta=access_token_expires
    )
    
    user = await user_collection.find_one({"email": form_data.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user["name"]}
