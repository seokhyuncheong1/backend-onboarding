from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from app.common.config import settings
from app.common.abort import abort_response
from app.common.path_validator import url_pattern_check
from app.service.jwt import JWTService
from app.mapper.user import UserMapper


base_url = "api/v1"

class LoginCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_path: str = request.url.path

        #검사 대상 경로가 아니면 건너뜀
        if not url_pattern_check(request_path):
            print(">>>>>>not check path<<<<<<<")
            return await call_next(request)

        if not "access_token" in request.cookies.keys():
            return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")

        access_token: str | None = request.cookies["access_token"]
        if access_token is None:
            return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")

        try:
            user_id: str = await JWTService.verify_token(access_token)
            if not UserMapper.exist_user_by_user_id(user_id):
                return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")

            return await call_next(request)
        except jwt.ExpiredSignatureError:
            #access_token 만료로 refresh_token 만료 체크
            try:
                if not "refresh_token" in request.cookies.keys():
                    return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")

                refresh_token: str = request.cookies["refresh_token"]
                refresh_id: str = await JWTService.verify_token(refresh_token)
                if refresh_id is None:
                    return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")

                #새 access token 발급 진행
                refresh_user_id: str = refresh_id.split(".")[0]
                if not UserMapper.exist_user_by_user_id(refresh_user_id):
                    return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")

                new_access_token: str = await JWTService.encode_token(refresh_user_id, settings.ACCESS_TOKEN_EXPIRES_IN)

                response: Response = await call_next(request)
                response.set_cookie("access_token", new_access_token)

                return response
            except:
                return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")
        except:
            return abort_response(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")
