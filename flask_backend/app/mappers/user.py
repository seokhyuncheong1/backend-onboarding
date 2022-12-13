from flask_restx.errors import abort, HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.user import User


class UserMapper:
    def find_user_by_user_id(db_session: Session, user_id: str) -> User:
        try:
            return db_session.query(User) \
                .filter(User.user_id == user_id) \
                .one()
        except NoResultFound:
            abort(401, "존재하지 않는 회원입니다.")