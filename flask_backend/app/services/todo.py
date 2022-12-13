from typing import List

from app.common.services.db import DBService
from app.mappers.todo import TodoMapper
from app.models.todo import Todo


class TodoService(DBService):
    def get_todos(self, user_id: str):
        todo_list: List[Todo] = TodoMapper.find_todos_by_user_id(self.db_session, user_id)

        return list(map(lambda todo: todo.__to_dict__(), todo_list))
