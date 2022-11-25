from fastapi import status, HTTPException
from app.schemas.request.auth import SignupRequest
import bcrypt

from app.mapper.user import UserMapper
from app.models.user import User


class AuthService:
    async def signup(signup_info: SignupRequest):
        if signup_info.user_password != signup_info.user_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="비밀번호가 일치하지 않습니다."
            )

        hash_password: str = bcrypt.hashpw(
            signup_info.user_password.encode("utf-8"), 
            bcrypt.gensalt()
            ).decode("utf-8")

        signup_user: User = User(signup_info.user_id, hash_password)
        await UserMapper.create_user(signup_user)