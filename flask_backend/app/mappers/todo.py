from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.models.user import User


class TodoMapper:
    def find_todos_by_user_id(db_session: Session, user_id: str):
        try:
            return db_session.query(Todo) \
                .join(Todo.user) \
                .filter(User.user_id == user_id) \
                .all()
        except:
            db_session.rollback()
