from fastapi import APIRouter
from app.schemas.response.test import TestResponse


router = APIRouter()


@router.get('/id/{id}')
async def return_id(id: int) -> TestResponse:
    return TestResponse(id=id)
