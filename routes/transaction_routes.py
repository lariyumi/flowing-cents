from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dependencies import db_session, validate_token
from schemas import TransactionSchema, TagSchema
from models import Transaction, Account, User, Tag, TransactionTag

transaction_router = APIRouter(prefix="/transaction", tags=["transaction"], dependencies=[Depends(validate_token)])

def checking_account_user(account_id: int, session, user):
    account = session.query(Account).filter(account_id == Account.id).first()

    if not account:
        raise HTTPException(status_code=400, detail="Informed account doesn't exist")
    elif account.user != user.id:
        raise HTTPException(status_code=403, detail="User linked to the account doesn't match authenticated user")
    else:
        return account

@transaction_router.get("/")
async def all_transactions(session: Session = Depends(db_session), user: User = Depends(validate_token)):
    accounts = session.query(Account).filter(Account.user == user.id).all()
    transactions = [account.transactions for account in accounts]

    return {
        "transactions": transactions
    }

@transaction_router.post("/", status_code=201)
async def add_transaction(transaction_schema: TransactionSchema, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    account = checking_account_user(transaction_schema.account, session, user)
    new_transaction = Transaction(transaction_schema.amount, transaction_schema.date, transaction_schema.type_transaction, transaction_schema.account)

    session.add(new_transaction)
    account.calculate_balance(new_transaction.amount, new_transaction.type_transaction)
    
    for tag in transaction_schema.tags:
        find_tag = session.query(Tag).filter(tag.name == Tag.name).filter(Tag.user == user.id).first()

        if not find_tag:
            new_tag = Tag(tag.name, user.id)
            session.add(new_tag)
            session.flush()
            
            new_transaction_tag = TransactionTag(new_tag.id, new_transaction.id)
            session.add(new_transaction_tag)
        else:
            new_transaction_tag = TransactionTag(find_tag.id, new_transaction.id)
            session.add(new_transaction_tag)

    session.commit()

    return {
        "message": "Transaction successfully registered"
    }

@transaction_router.get("/{transaction_id}")
async def get_transaction(transaction_id: int, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    transaction = session.query(Transaction).filter(transaction_id == Transaction.id).first()
    if not transaction:
        raise HTTPException(status_code=400, detail="Transaction not found")

    account = checking_account_user(transaction.account, session, user)

    return {
        "amount": transaction.amount,
        "date": transaction.date,
        "type_transaction": transaction.type_transaction,
        "account": transaction.account
    }

@transaction_router.put("/{transaction_id}")
async def edit_transaction(transaction_id: int, transaction_schema: TransactionSchema, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    transaction = session.query(Transaction).filter(transaction_id == Transaction.id).first()

    if not transaction:
        raise HTTPException(status_code=400, detail="Transaction not found")

    account = checking_account_user(transaction_schema.account, session, user)

    new_type_transaction = "INCOME" if transaction.type_transaction == "EXPENSE" else "EXPENSE"

    # Take off the value of the transaction from the balance account
    account.calculate_balance(transaction.amount, new_type_transaction)

    # Apply the new transaction value
    account.calculate_balance(transaction_schema.amount, transaction_schema.type_transaction)

    transaction.amount = transaction_schema.amount
    transaction.date = transaction_schema.date
    transaction.type_transaction = transaction_schema.type_transaction
    transaction.account = transaction_schema.account

    session.commit()

    return {
        "message": "Transaction successfully edited"
    }

@transaction_router.delete("/delete/{transaction_id}")
async def delete_transaction(transaction_id: int, session: Session = Depends(db_session), user: User = Depends(validate_token)):
    transaction = session.query(Transaction).filter(transaction_id == Transaction.id).first()

    if not transaction:
        raise HTTPException(status_code=400, detail="Specified transaction not found")

    account = checking_account_user(transaction.account, session, user)

    account.calculate_balance(-transaction.amount, transaction.type_transaction)
    session.delete(transaction)
    session.commit()

    return {
        "message": "Transaction successfully deleted"
    }