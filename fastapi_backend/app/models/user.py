from sqlalchemy import Column, Integer, String
from app.common.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment='사용자 pk')
    user_id = Column(String(20), nullable=False,
                     unique=True, comment='사용자의 아이디')
    user_password = Column(String(200), nullable=False,
                           comment='사용자의 암호화된 비밀번호')

    def __init__(self, id: int, user_id: str, user_password: str):
        self.id = id
        self.user_id = user_id
        self.user_password = user_password

    def __init__(self, user_id: str, user_password: str):
        self.user_id = user_id
        self.user_password = user_password

    def __init__(self, id: int):
        self.id = id
