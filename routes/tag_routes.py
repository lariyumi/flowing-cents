from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dependencies import db_session, validate_token
from schemas import TagSchema
from models import Tag, User

tag_router = APIRouter(prefix="/tag", tags=["tag"], dependencies=[Depends(validate_token)])

@tag_router.get("/")
async def all_tags(session: Session = Depends(db_session), user: User = Depends(validate_token)):
    tags = session.query(Tag).filter(user.id == Tag.user).all()

    return {
        "tags": tags
    }

# @tag_router.delete("/{tag_id}")
# async def delete_tag(tag_id: int, session: Session = Depends(db_session)):
#     tag = session.query(Tag).filter(tag_id == Tag.id).first()