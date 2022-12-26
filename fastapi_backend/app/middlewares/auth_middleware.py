from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional, Tuple

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from app.common.config import settings
from app.common.abort import abort_response
from app.common.path_validator import url_pattern_check
from app.service.jwt import JWTService
from app.mapper.user import UserMapper


base_url = "api/v1"


class AuthMiddleware(AuthenticationBackend):
    async def authenticate(self, request: HTTPConnection) -> Optional[Tuple["AuthCredentials", "BaseUser"]]:
        request_path: str = request.url.path

        #검사 대상 경로가 아니면 건너뜀
        if not url_pattern_check(request_path):
            print(">>>>>>not check path<<<<<<<")
            return

        if not "Authorization" in request.headers:
            raise AuthenticationError("로그인이 필요합니다.")

        auth = request.headers["Authorization"]
        scheme, access_token = get_authorization_scheme_param(auth)
        if scheme != "Bearer":
            raise AuthenticationError("로그인이 필요합니다.")

        try:
            user_id = await JWTService.verify_token(access_token)

            is_exist_user = UserMapper.exist_user_by_user_id(user_id)
            if not is_exist_user:
                raise AuthenticationError("알 수 없는 유저입니다.")
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("만료된 토큰입니다.")
        except jwt.InvalidSignatureError:
            raise AuthenticationError("알 수 없는 토큰입니다.")
        
        return access_token, user_id
