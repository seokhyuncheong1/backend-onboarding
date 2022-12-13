from fastapi import status
from typing import List

from app.mapper.todo import TodoMapper
from app.mapper.asyncro.todo import AsyncTodoMapper
from app.schemas.request.todo import TodoRequest
from app.schemas.response.todo import TodoDTO
from app.models.todo import Todo
from app.common.abort import abort_exception
from app.common.services.db import AsyncDBService


class TodoService(AsyncDBService):
    async def add_todo(self, todo: TodoRequest, user_id: str):       
        await AsyncTodoMapper.create_todo(self.db_session, user_id, todo.title, todo.detail)

    async def get_todo_list(self, user_id: str) -> List[TodoDTO]:
        todo_list: List[TodoDTO] = await AsyncTodoMapper.find_todos_by_user_id(self.db_session, user_id)

        return todo_list

    async def update_todo(self, todo_id: int, user_id: str, todo: TodoRequest):
        await AsyncTodoMapper.update_todo(self.db_session, todo_id, user_id, todo)

    async def delete_todo(self, todo_id: int, user_id: str):
        await AsyncTodoMapper.delete_todo(self.db_session, todo_id, user_id)

