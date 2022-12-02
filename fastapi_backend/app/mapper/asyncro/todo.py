from fastapi import status
from typing import List
from sqlalchemy import select, update
from sqlalchemy.engine import Result

from app.common.db import async_db_session
from app.common.abort import abort_exception
from app.models.todo import Todo
from app.models.user import User
from app.schemas.request.todo import TodoRequest
from app.schemas.response.todo import TodoDTO


class AsyncTodoMapper:
    async def find_todos_by_user_id(user_id: str) -> List[TodoDTO]:
        query = (
            select(Todo.title, Todo.detail, User.user_id, Todo.created_at)
            .join(Todo.user)
            .where(User.user_id == user_id)
            .order_by(Todo.created_at.desc())
        )
        result: Result = await async_db_session.execute(query)

        print(async_db_session.registry.registry)
        await async_db_session.remove()

        return result.all()

    async def update_todo(todo_id: int, user_id: str, todo: TodoRequest):
        #TODO update문 수정하기
        query = (
            update(Todo)
            .where(Todo.id == todo_id)
            .where(Todo.user_id == User.id)
            .where(User.user_id == user_id)
            .values(todo.__to_dict__())
        )

        print(query)

        try:
            await async_db_session.execute(query)
            print(async_db_session.registry.registry)
        except:
            abort_exception(status.HTTP_406_NOT_ACCEPTABLE, "수정할 수 없습니다.")
        finally:
            await async_db_session.remove()