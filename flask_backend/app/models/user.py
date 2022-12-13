from app.common.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, comment='사용자 pk')
    user_id = db.Column(db.String(20), nullable=False,
                     unique=True, comment='사용자의 아이디')
    user_password = db.Column(db.String(200), nullable=False,
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

    def __to_dict__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_password": self.user_password
        }
