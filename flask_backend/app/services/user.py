from flask_restx.errors import abort, HTTPStatus
import bcrypt

from app.common.services.db import DBService
from app.common.services.jwt import JWTService
from app.mappers.user import UserMapper
from app.models.user import User
from app.common.config import Config


class UserService(DBService):
    def login_user(self, user_id: str, user_password: str):
        ex_user: User = UserMapper.find_user_by_user_id(
            self.db_session, user_id)

        is_verified: bool = bcrypt.checkpw(user_password.encode("utf-8"),
                                           ex_user.user_password.encode("utf-8"))
        if not is_verified:
            abort(401, "비밀번호가 일치하지 않습니다.")

        access_token: str = JWTService.encode_token(user_id, Config.ACCESS_TOKEN_EXPIRES_IN)
        refresh_token: str = JWTService.encode_token(user_id + ".refresh", Config.REFRESH_TOKEN_EXPIRES_IN)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        
