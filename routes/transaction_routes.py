from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dependencies import db_session, validate_token
from schemas import TransactionSchema, TagSchema, TransactionTagSchema
from models import Transaction, Tag, TransactionTag, Account, User

transaction_router = APIRouter(prefix="/transaction", tags=["transaction"], dependencies=[Depends(validate_token)])

@transaction_router.get("/")
async def all_transactions(session: Session = Depends(db_session), user: User = Depends(validate_token)):
    accounts = session.query(Account).filter(Account.user == user.id).all()
    transactions = [account.transactions for account in accounts]

    return {
        "transactions": transactions
    }