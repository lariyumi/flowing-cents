from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    active: Optional[bool]

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

    class Config:
        from_attributes = True