from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.common.db import Base
from app.models.user import User


class Todo(Base):
    __tablename__ = 'todos'

    id: int = Column(Integer, primary_key=True, comment='todo pk')
    title: str = Column(String(20), nullable=False, comment='todo 제목')
    detail: str = Column(String(100), comment='todo 상세기술')
    user_id: int = Column(Integer, ForeignKey('users.id'))
    user: User = relationship("User")
    created_at: datetime = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, title, detail, user):
        self.title = title
        self.detail = detail
        self.user = user
