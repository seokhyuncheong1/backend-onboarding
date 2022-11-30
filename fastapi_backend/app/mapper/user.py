from fastapi import status, HTTPException
from typing import Optional

from app.common.db import get_db_session
from app.models.user import User


class UserMapper:
    def create_user(signup_user: User) -> None:

        with get_db_session() as session:
            try:
                session.add(signup_user)
                session.commit()
            except:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="이미 가입된 회원입니다."
                )


    def find_user_by_user_id(user_id: str) -> Optional[User]:
        ex_user: Optional[User] = None

        with get_db_session() as session:
            try:
                ex_user = session.query(User).filter_by(user_id=user_id).one()
            except:
                print('존재하지 않는 회원입니다.')

        return ex_user


    def exist_user_by_user_id(user_id: str) -> bool:
        result: bool = False

        with get_db_session() as session:
            q = session.query(User).filter_by(user_id=user_id).exists()
            result = session.query(q).scalar()

        return result