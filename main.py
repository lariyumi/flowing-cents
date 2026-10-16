from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/login/auth-form")

from routes.user_routes import user_router
from routes.account_routes import account_router
from routes.transaction_routes import transaction_router
from routes.tag_routes import tag_router

app.include_router(user_router)
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(tag_router)