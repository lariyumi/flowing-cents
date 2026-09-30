from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

from routes.user_routes import user_router

app.include_router(user_router)