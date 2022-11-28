from fastapi import status, HTTPException

from app.common.db import get_db_session
from app.models.user import User


class UserMapper:
    def create_user(signup_user: User):
        session = get_db_session()

        try:
            session.add(signup_user)
            session.commit()
        except:
            session.close()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이미 가입된 회원입니다."
            )
        
        session.close()


    def find_user_by_user_id(user_id: str) -> User:
        session = get_db_session()

        ex_user: User = None

        try:
            ex_user = session.query(User).filter_by(user_id=user_id).one()
        except:
            print('존재하지 않는 회원입니다.')
        finally:
            session.close()

        return ex_user
            