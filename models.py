import enum
from sqlalchemy import create_engine, Enum, Column, String, Integer, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

db = create_engine("sqlite:///database/database.db")

Base = declarative_base()

class TypeTransaction(str, enum.Enum):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    active = Column("active", Boolean, default=True)

    def __init__(self, name, email, password, active=True):
        self.name = name
        self.email = email
        self.password = password
        self.active = active

class Account(Base):
    __tablename__ = "accounts"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name_financial_institution = Column("name_financial_institution", String, nullable=False)
    balance = Column("balance", Float, nullable=False)
    user = Column("user", ForeignKey("users.id"))
    transactions = relationship("Transaction", cascade="all, delete")

    def __init__(self, name_financial_institution, balance, user):
        self.name_financial_institution = name_financial_institution
        self.balance = balance
        self.user = user

    def calculate_balance(self, amount:float, op: str):
        if op == "EXPENSE":
            self.balance -= amount
        else:
            self.balance += amount

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    amount = Column("amount", Float, nullable=False)
    date = Column("date", Date, nullable=False)
    type_transaction = Column("type_transaction", Enum(TypeTransaction), nullable=False)
    account = Column("account", ForeignKey("accounts.id"))
    tags = relationship("TransactionTag", back_populates="transaction")

    def __init__(self, amount, date, type_transaction, account):
        self.amount = amount
        self.date = date
        self.type_transaction = type_transaction
        self.account = account

class Tag(Base):
    __tablename__ = "tags"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    transactions = relationship("TransactionTag", back_populates="tag")
    user = Column("user", ForeignKey("users.id"))

    def __init__(self, name, user):
        self.name = name
        self.user = user

class TransactionTag(Base):
    __tablename__ = "transaction_tag"

    tag_id = Column("tag", ForeignKey("tags.id"), primary_key=True)
    transaction_id = Column("transaction", ForeignKey("transactions.id"), primary_key=True)
    transaction = relationship("Transaction", back_populates="tags")
    tag = relationship("Tag", back_populates="transactions")

    def __init__(self, tag_id, transaction_id):
        self.tag_id = tag_id
        self.transaction_id = transaction_id