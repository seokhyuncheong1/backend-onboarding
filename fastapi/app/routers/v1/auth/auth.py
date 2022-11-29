from fastapi import APIRouter
from app.service.auth import AuthService
from app.schemas.request.auth import (
    SignupRequest,
    LoginRequest
)
from app.schemas.response.auth import LoginResponse


router = APIRouter()


@router.post('/signup')
async def signup(signup_info: SignupRequest):
    await AuthService.signup(signup_info)
    return { 'message': 'ok' }


@router.post('/login', response_model=LoginResponse)
async def login(login_info: LoginRequest):
    return await AuthService.login(login_info)