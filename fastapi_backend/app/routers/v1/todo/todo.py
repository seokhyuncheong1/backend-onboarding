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
    async with TodoService() as todoService:
        todoService: TodoService
        user_id: str = await JWTService.verify_token(request.cookies['access_token'])
        await todoService.add_todo(todo, user_id)


@router.get('/')
async def get_todo_list(request: Request):
    user_id: str = await JWTService.verify_token(request.cookies['access_token'])
    
    async with TodoService() as todoService:
        todoService: TodoService
        todo_list: List[TodoDTO] = await todoService.get_todo_list(user_id)
    
    return todo_list


@router.patch('/{todo_id}')
async def update_todo(todo_id: int, todo: TodoRequest, request: Request):
    async with TodoService() as todoService:
        todoService: TodoService
        user_id: str = await JWTService.verify_token(request.cookies['access_token'])
        return await todoService.update_todo(todo_id, user_id, todo)


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int, request: Request):
    user_id: str = await JWTService.verify_token(request.cookies['access_token'])

    async with TodoService() as todoService:
        todoService: TodoService
        await todoService.delete_todo(todo_id, user_id)
