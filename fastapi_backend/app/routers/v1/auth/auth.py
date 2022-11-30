from fastapi import APIRouter, Request, Response
from app.service.auth import AuthService
from app.mapper.user import UserMapper
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
async def login(login_info: LoginRequest, response: Response):
    jwt_token: LoginResponse = await AuthService.login(login_info)
    response.set_cookie("access_token", jwt_token.access_token)
    response.set_cookie("refresh_token", jwt_token.refresh_token)

    return jwt_token


@router.get('/exist/{user_id}')
async def exist_user_id(user_id: str):
    return UserMapper.exist_user_by_user_id(user_id)