from app.common.db import db
from app.models.user import User
from datetime import datetime


class Todo(db.Model):
    __tablename__ = 'todos'

    id: int = db.Column(db.Integer, primary_key=True, comment='todo pk')
    title: str = db.Column(db.String(20), nullable=False, comment='todo 제목')
    detail: str = db.Column(db.String(100), comment='todo 상세기술')
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'))
    user: User = db.relationship("User")
    created_at: datetime = db.Column(db.DateTime(timezone=True))

    def __init__(self, title, detail, user):
        self.title = title
        self.detail = detail
        self.user = user

    def __to_dict__(self):
        return {
            "id": self.id,
            "title": self.title,
            "detail": self.detail,
            "user_id": self.user_id,
            "created_at": f'{self.created_at.year}-{self.created_at.month}-{self.created_at.day} {self.created_at.hour}:{self.created_at.minute}:{self.created_at.second}'
        }
