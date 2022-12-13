from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.common.db import Base


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, comment='todo pk')
    title = Column(String(20), nullable=False, comment='todo 제목')
    detail = Column(String(100), comment='todo 상세기술')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")
    created_at = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, title, detail, user):
        self.title = title
        self.detail = detail
        self.user = user
