from fastapi import APIRouter, Request
from typing import List

from app.mapper.todo import TodoMapper
from app.service.todo import TodoService
from app.service.jwt import JWTService
from app.schemas.request.todo import TodoRequest
from app.schemas.response.todo import TodoDTO


router = APIRouter()


@router.post('/')
async def add_todo(todo: TodoRequest, request: Request):
    user_id: str = await JWTService.verify_token(request.cookies['access_token'])
    await TodoService.add_todo(todo, user_id)


@router.get('/user_id/{user_id}')
async def get_todo_list(user_id: str):
    todo_list: List[TodoDTO] = TodoMapper.find_todos_by_user_id(user_id)

    return todo_list


@router.patch('/{todo_id}')
async def update_todo(todo_id: int, todo: TodoRequest, request: Request):
    print(f'todo: {todo}')
    user_id: str = await JWTService.verify_token(request.cookies['access_token'])
    return await TodoService.update_todo(todo_id, user_id, todo)


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int, request: Request):
    user_id: str = await JWTService.verify_token(request.cookies['access_token'])
    return TodoMapper.delete_todo(todo_id, user_id)
