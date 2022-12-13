from flask import request, abort
from functools import wraps
from jwt import ExpiredSignatureError

from app.common.config import Config
from app.common.services.jwt import JWTService


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not "access_token" in request.cookies.keys() or not "refresh_token" in request.cookies.keys():
            abort(404, "로그인이 필요합니다.")

        try:
            access_token: str = request.cookies.get("access_token")
            user_id = JWTService.verify_token(access_token)
        except ExpiredSignatureError:
            print("액세스 토큰이 만료되었습니다.")

            try:
                refresh_token: str = request.cookies.get("refresh_token")
                refresh_user_id: str = JWTService.verify_token(refresh_token)
                user_id: str = refresh_user_id.split(".")[0]

                new_access_token: str = JWTService.encode_token(
                    user_id, Config.ACCESS_TOKEN_EXPIRES_IN)                
            except Exception as e:
                print(e)
                print("리프레쉬 토큰이 만료되었습니다. 재로그인이 필요합니다.")
                abort(404, "로그인이 필요합니다.")
        except:
            print("잘못된 액세스 토큰입니다.")
            abort(404, "로그인이 필요합니다.")

        return func(*args, **kwargs)

    return wrapper
