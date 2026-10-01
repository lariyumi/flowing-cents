from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Annotated

class UserSchema(BaseModel):
    name: Annotated[str, Field(min_length=2)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]

    class Config:
        from_attributes = True

class AccountSchema(BaseModel):
    name_financial_institution: Annotated[str, Field(min_length=2)]
    balance: float
    user: Annotated[int, Field(ge=0)]

    class Config: 
        from_attributes = True