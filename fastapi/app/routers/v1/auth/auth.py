from fastapi import APIRouter
from app.mapper.user import UserMapper

from app.schemas.request.auth import SignupRequest


router = APIRouter()


@router.post('/signup')
async def signup(signup_user: SignupRequest):
    print(signup_user)
    result = await UserMapper.create_user(signup_user.user_id, signup_user.user_password)

    print(result)

    return { 'message': 'ok' }

