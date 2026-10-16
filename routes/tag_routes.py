from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dependencies import db_session, validate_token
from schemas import TagSchema
from models import Tag

tag_router = APIRouter(prefix="/tag", tags=["tag"], dependencies=[Depends(validate_token)])

@tag_router.get("/")
async def all_tags(session: Session = Depends(db_session)):
    tags = session.query(Tag).all()

    return {
        "tags": tags
    }