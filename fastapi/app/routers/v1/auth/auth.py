from fastapi import APIRouter
from app.service.auth import AuthService

from app.schemas.request.auth import SignupRequest


router = APIRouter()


@router.post('/signup')
async def signup(signup_info: SignupRequest):
    await AuthService.signup(signup_info)
    return { 'message': 'ok' }