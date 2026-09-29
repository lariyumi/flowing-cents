import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema
from dependencies import db_session
from models import User
from sqlalchemy.orm import Session
from pydantic import ValidationError

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/create-account")
async def create_account(user_schema: UserSchema, session: Session = Depends(db_session)):
    user = session.query(User).filter(User.email == user_schema.email).first()

    if user:
        raise HTTPException(status_code=400, detail="Email already used by an existing user")
    else:
        bytes_password = user_schema.password.encode("utf-8")
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(password=bytes_password, salt=salt)
        try:
            print("Entrou try")
            new_user = User(user_schema.name, user_schema.email, encrypted_password, user_schema.active)
        except ValidationError as e:
            return {
                "errors": [err.detail.sg for err in e]
            }

        session.add(new_user)
        session.commit()

        return {
            "message": f"User successfully registered"
        }