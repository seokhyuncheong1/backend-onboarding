from fastapi import status, Depends
from typing import List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import join
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.engine.result import ChunkedIteratorResult

from app.common.abort import abort_exception
from app.models.todo import Todo
from app.models.user import User
from app.schemas.request.todo import TodoRequest
from app.schemas.response.todo import TodoDTO


class AsyncTodoMapper:
    async def find_todos_by_user_id(session: AsyncSession, user_id: str) -> List[TodoDTO]:
        query = (
            select(Todo.title, Todo.detail, User.user_id, Todo.created_at)
            .join(Todo.user)
            .where(User.user_id == user_id)
            .order_by(Todo.created_at.desc())
        )
        result: Result = await session.execute(query)

        return result.all()

    async def create_todo(session: AsyncSession, user_id: str, title: str, detail: str):
        try:
            user_pk_query = select(User) \
                .where(User.user_id == user_id)

            result: Result = await session.execute(user_pk_query)
            user: User = result.scalars().first()

            todo: Todo = Todo(title, detail, user)
            session.add(todo)
        except:
            abort_exception(status.HTTP_406_NOT_ACCEPTABLE, "추가할 수 없습니다.")

    async def update_todo(session: AsyncSession, todo_id: int, user_id: str, todo: TodoRequest):
        try:
            query = select(User.id) \
                .where(User.user_id == user_id)

            result = await session.execute(query)
            user_pk: int = result.scalar()

            query = update(Todo) \
                .values(todo.__to_dict__()) \
                .where(Todo.id == todo_id) \
                .where(Todo.user_id == user_pk)

            print(f'update sql: {query}')
            await session.execute(query)
        except:
            abort_exception(status.HTTP_406_NOT_ACCEPTABLE, "수정할 수 없습니다.")

    async def delete_todo(session: AsyncSession, todo_id: int, user_id: str):
        try:
            query = f'''
                DELETE
                FROM todos
                USING users
                WHERE todos.user_id = users.id
                AND todos.id = :todo_id
                AND users.user_id = :user_id
            '''
            
            await session.execute(query, {
                "todo_id": todo_id,
                "user_id": user_id
            })
        except:
            abort_exception(status.HTTP_406_NOT_ACCEPTABLE, "삭제할 수 없습니다.")
