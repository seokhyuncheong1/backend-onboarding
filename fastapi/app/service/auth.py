from fastapi import status, HTTPException
from typing import Optional
import bcrypt
import jwt
from datetime import datetime, timedelta

from app.common.config import settings
from app.schemas.request.auth import (
    SignupRequest,
    LoginRequest
)
from app.schemas.response.auth import LoginResponse
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
        UserMapper.create_user(signup_user)


    async def login(login_info: LoginRequest) -> LoginResponse:
        ex_user: Optional[User] = UserMapper.find_user_by_user_id(login_info.user_id)

        if ex_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="존재하지 않는 회원입니다."
            )
        
        is_verified: bool = bcrypt.checkpw(login_info.user_password.encode("utf-8"),
                                           ex_user.user_password.encode("utf-8"))
        if not is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 일치하지 않습니다."
            )

        access_payload = {
            "user_id": ex_user.user_id,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
        }
        access_token = jwt.encode(access_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        
        refresh_payload = {
            "user_id": f'{ex_user.user_id}.refresh',
            "exp": datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN)
        }
        refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)
