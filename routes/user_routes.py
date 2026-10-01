import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from dependencies import db_session
from models import User

user_router = APIRouter(prefix="/user", tags=["user"])

def authenticate_user(email: str, password: str, session):
    user = session.query(User).filter(User.email == email).first()

    if not user:
        return False
    elif not bcrypt.checkpw(password.encode("utf-8"), user.password):
        return False
    return user

def create_token(user_id: int, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = str(datetime.now(timezone.utc) + token_duration)
    dic_info = {"sub": str(user_id), "exp_date": expiration_date}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    return encoded_jwt

@user_router.post("/create-account", status_code=201)
async def create_account(user_schema: UserSchema, session: Session = Depends(db_session)):
    user = session.query(User).filter(User.email == user_schema.email).first()

    if user:
        raise HTTPException(status_code=400, detail="Email already used by an existing user")
    else:
        bytes_password = user_schema.password.encode("utf-8")
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(password=bytes_password, salt=salt)

        new_user = User(user_schema.name, user_schema.email, encrypted_password, user_schema.active)

        session.add(new_user)
        session.commit()

        return {
            "message": f"User successfully registered"
        }

@user_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(db_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credentials")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=14))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@user_router.post("/login/auth-form")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(db_session)):
    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credentials")
    else:
        access_token = create_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }