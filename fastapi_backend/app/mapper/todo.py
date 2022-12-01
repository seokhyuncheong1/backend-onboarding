from fastapi import status, HTTPException
from typing import List
from sqlalchemy import delete
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.exc import NoResultFound

from app.common.db import get_db_session
from app.common.abort import abort_exception
from app.models.todo import Todo
from app.models.user import User
from app.schemas.request.todo import TodoRequest
from app.schemas.response.todo import TodoDTO


class TodoMapper:
    def create_todo(user_id: str, title: str, detail: str):
        with get_db_session() as session:
            try:
                print('>>>>>>>>>>>>>>create_todo')
                author: User = session.query(User).filter(
                    User.user_id == user_id).one()

                session.add(Todo(title, detail, author))
                session.commit()
            except NoResultFound:
                abort_exception(status.HTTP_401_UNAUTHORIZED, "존재하지 않는 회원입니다.")

    def find_todos_by_user_id(user_id: str) -> List[TodoDTO]:
        print(">>>>>>>>>>>>>find_todos")
        todo_list: List[TodoDTO] = []
        with get_db_session() as session:
            todo_list = session.query(Todo.title, Todo.detail, User.user_id, Todo.created_at).join(
                Todo.user).filter(User.user_id == user_id).all()

            print(type(todo_list[0]))

        return todo_list

    def update_todo(todo_id: int, user_id: str, todo: TodoRequest):
        with get_db_session() as session:
            try:
                ex_todo: Todo = session.query(Todo).join(Todo.user).filter(
                    Todo.id == todo_id
                ).filter(
                    User.user_id == user_id
                ).one()

                ex_todo.title = todo.title
                ex_todo.detail = todo.detail
                session.commit()
            except:
                abort_exception(status.HTTP_406_NOT_ACCEPTABLE, "수정이 불가능합니다.")

    def delete_todo(todo_id: int, user_id: str):
        with get_db_session() as session:
            try:
                sql = delete(Todo).where(Todo.id == todo_id and User.user_id == user_id)
                session.execute(sql)
                # target_todo: Todo = session.query(Todo).join(Todo.user).filter(
                #     Todo.id == todo_id
                # ).filter(
                #     User.user_id == user_id
                # ).one()

                # session.delete(target_todo)
                session.commit()
            except:
                abort_exception(status.HTTP_406_NOT_ACCEPTABLE, "삭제가 불가능합니다.")
