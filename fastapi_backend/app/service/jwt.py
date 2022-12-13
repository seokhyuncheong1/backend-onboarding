from fastapi import status, HTTPException
import jwt
from datetime import datetime, timedelta

from app.common.config import settings


class JWTService:
    async def encode_token(user_id: str, expire_minute: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expire_minute)
        }

        return jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)


    async def verify_token(token: str):
        decode_token = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return decode_token["user_id"]
