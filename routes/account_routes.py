from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dependencies import db_session, validate_token
from schemas import AccountSchema
from models import User, Account

account_router = APIRouter(prefix="/account", tags=["account"], dependencies=[Depends(validate_token)])

@account_router.get("/")
async def list_accounts(session: Session = Depends(db_session), user: User = Depends(validate_token)):
    accounts = session.query(Account).filter(Account.user == user.id).all()

    return {
        "accounts": accounts
    }

@account_router.post("/create-account", status_code=201)
async def add_account(account_schema: AccountSchema, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    if account_schema.user != user.id:
        raise HTTPException(status_code=403, detail="User linked to the account doesn't match authenticated user")

    new_account = Account(account_schema.name_financial_institution, account_schema.balance, account_schema.user)

    session.add(new_account)
    session.commit()

    return {
        "message": "Account successfully created"
    }

@account_router.get("/{account_id}")
async def show_specific_account(account_id: int, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    account = session.query(Account).filter(account_id == Account.id).first()

    if not account:
        raise HTTPException(status_code=400, detail="Requested account doesn't exist")
    elif user.id != account.user:
        raise HTTPException(status_code=403, detail="You don't have permission to view another user's account")
    else:
        return {
            "name_financial_institution": account.name_financial_institution,
            "balance": account.balance
        }

@account_router.put("/{account_id}")
async def edit_account(account_id: int, account_schema: AccountSchema, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    account = session.query(Account).filter(account_id == Account.id).first()

    if not account:
        raise HTTPException(status_code=400, detail="Requested account doesn't exist")
    elif user.id != account.user:
        raise HTTPException(status_code=403, detail="You don't have permission to edit another user's account")
    else:
        account.name_financial_institution = account_schema.name_financial_institution
        account.balance = account_schema.balance

        session.commit()

        return {
            "message": "Account successfully edited"
        }

@account_router.delete("/delete/{account_id}")
async def delete_account(account_id: int, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    account = session.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=400, detail="Requested account doesn't exist")
    elif user.id != account.user:
        raise HTTPException(status_code=403, detail="You don't have permission to delete another user's account")
    else:
        session.delete(account)
        session.commit()

        return {
            "message": "Account successfully deleted"
        }