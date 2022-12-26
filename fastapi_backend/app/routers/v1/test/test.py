from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.common.db import get_db_session
from app.schemas.response.test import TestResponse
from app.models.user import User


router = APIRouter()


@router.get('')
async def test():
    session: Session = get_db_session()
    return session.query(User) \
        .filter(User.user_id == 'test11') \
        .first()


@router.get('/id/{id}')
async def return_id(id: int) -> TestResponse:
    return TestResponse(id=id)
