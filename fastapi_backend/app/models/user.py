from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.common.db import Base

class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, comment='사용자 pk')
    user_id: str = Column(String(20), nullable=False,
                     unique=True, comment='사용자의 아이디')
    user_password: str = Column(String(200), nullable=False,
                           comment='사용자의 암호화된 비밀번호')
    # todos = relationship("Todo", backref="user")

    def __init__(self, user_id: str, user_password: str):
        self.user_id = user_id
        self.user_password = user_password

    def __to_dict__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_password": self.user_password
        }
