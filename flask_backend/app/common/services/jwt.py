import jwt
from datetime import datetime, timedelta

from app.common.config import Config


class JWTService:
    def encode_token(user_id: str, expire_minute: int) -> str:
        print(f'type: {type(expire_minute)}, value: {expire_minute}')
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expire_minute)
        }

        return jwt.encode(payload, Config.JWT_SECRET_KEY, Config.JWT_ALGORITHM)

    def verify_token(token: str):
        decode_token = jwt.decode(
            token, Config.JWT_SECRET_KEY, Config.JWT_ALGORITHM)
        return decode_token["user_id"]
