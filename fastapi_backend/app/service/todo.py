from fastapi import status

from app.mapper.todo import TodoMapper
from app.schemas.request.todo import TodoRequest
from app.models.todo import Todo
from app.common.abort import abort_exception


class TodoService:
    async def add_todo(todo: TodoRequest, user_id: str):
        TodoMapper.create_todo(user_id, todo.title, todo.detail)

    async def update_todo(todo_id:int, user_id: str, todo: TodoRequest):
        TodoMapper.update_todo(todo_id, user_id, todo)

