from fastapi import status, HTTPException
from typing import Optional
import bcrypt

from app.common.config import settings
from app.common.abort import abort_exception
from app.schemas.request.auth import (
    SignupRequest,
    LoginRequest
)
from app.schemas.response.auth import LoginResponse
from app.service.jwt import JWTService
from app.mapper.user import UserMapper
from app.models.user import User


class AuthService:
    async def signup(signup_info: SignupRequest):
        if signup_info.user_password != signup_info.user_password_confirm:
            abort_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, "비밀번호가 일치하지 않습니다.")

        hash_password: str = bcrypt.hashpw(
            signup_info.user_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        signup_user: User = User(signup_info.user_id, hash_password)
        UserMapper.create_user(signup_user)


    async def login(login_info: LoginRequest) -> LoginResponse:
        ex_user: Optional[User] = UserMapper.find_user_by_user_id(login_info.user_id)

        if ex_user is None:
            abort_exception(status.HTTP_401_UNAUTHORIZED, "존재하지 않는 회원입니다.")
        
        is_verified: bool = bcrypt.checkpw(login_info.user_password.encode("utf-8"),
                                           ex_user.user_password.encode("utf-8"))
        if not is_verified:
            abort_exception(status.HTTP_401_UNAUTHORIZED, "비밀번호가 일치하지 않습니다.")

        access_token: str = await JWTService.encode_token(ex_user.user_id, settings.ACCESS_TOKEN_EXPIRES_IN)
        refresh_token: str = await JWTService.encode_token(f'{ex_user.user_id}.refresh', settings.REFRESH_TOKEN_EXPIRES_IN)

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)
