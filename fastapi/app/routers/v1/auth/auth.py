from fastapi import APIRouter
from app.service.auth import AuthService
from app.schemas.request.auth import (
    SignupRequest,
    LoginRequest
)


router = APIRouter()


@router.post('/signup')
async def signup(signup_info: SignupRequest):
    await AuthService.signup(signup_info)
    return { 'message': 'ok' }


@router.post('/login')
async def login(login_info: LoginRequest):
    await AuthService.login(login_info)
    return { 'message': 'ok' }