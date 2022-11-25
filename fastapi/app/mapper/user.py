from fastapi import status, HTTPException

from app.common.db import get_db_session
from app.models.user import User


class UserMapper:
    async def create_user(signup_user: User):
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