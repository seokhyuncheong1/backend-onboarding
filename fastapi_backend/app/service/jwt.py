from fastapi import status
import jwt
from datetime import datetime, timedelta

from app.common.config import settings
from app.common.abort import abort_exception


class JWTService:
    async def encode_token(user_id: str, expire_minute: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expire_minute)
        }

        return jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)


    async def verify_token(token: str) ->  str:
        decode_token = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return decode_token["user_id"]

    
    async def refresh_token(refresh_token: str) -> str:
        try:
            decode_token: str = await JWTService.verify_token(refresh_token)
            user_id, token_type = decode_token.split(".")

            if not token_type == "refresh":
                abort_exception(status.HTTP_401_UNAUTHORIZED, "잘못된 토큰입니다.")
        except jwt.ExpiredSignatureError:
            abort_exception(status.HTTP_401_UNAUTHORIZED, "만료된 토큰입니다.")
        except jwt.InvalidSignatureError:
            abort_exception(status.HTTP_401_UNAUTHORIZED, "잘못된 토큰입니다.")

        return await JWTService.encode_token(user_id, settings.ACCESS_TOKEN_EXPIRES_IN)
