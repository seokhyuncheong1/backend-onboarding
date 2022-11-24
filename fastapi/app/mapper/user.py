from app.common.db import get_db_session
from app.models.user import User



class UserMapper:
    async def create_user(user_id: str, user_password: str):
        user= User(user_id=user_id, user_password=user_password)

        session = get_db_session()
        session.add(user)

        session.commit()        

        session.close()