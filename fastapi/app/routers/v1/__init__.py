from fastapi import APIRouter
from .test import test


api_router = APIRouter()
api_router.include_router(test.router, prefix='/test')