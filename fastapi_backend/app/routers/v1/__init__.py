from fastapi import APIRouter
from .test import test
from .auth import auth
from .todo import todo


api_router = APIRouter()
api_router.include_router(test.router, prefix='/test')
api_router.include_router(auth.router, prefix='/auth')
api_router.include_router(todo.router, prefix='/todo')