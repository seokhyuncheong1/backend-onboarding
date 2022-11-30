from fastapi import APIRouter
from .test import test
from .auth import auth


api_router = APIRouter()
api_router.include_router(test.router, prefix='/test')
api_router.include_router(auth.router, prefix='/auth')