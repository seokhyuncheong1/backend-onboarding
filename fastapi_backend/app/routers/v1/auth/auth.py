from fastapi import APIRouter, Request, Response
from app.service.auth import AuthService
from app.mapper.user import UserMapper
from app.schemas.request.auth import (
    SignupRequest,
    LoginRequest
)
from app.schemas.request.auth import RefreshTokenRequest
from app.schemas.response.auth import LoginResponse
from app.service.jwt import JWTService


router = APIRouter()


@router.post('/signup')
async def signup(signup_info: SignupRequest):
    await AuthService.signup(signup_info)
    return { 'message': 'ok' }


@router.post('/login', response_model=LoginResponse)
async def login(login_info: LoginRequest):
    jwt_token: LoginResponse = await AuthService.login(login_info)
    return jwt_token


@router.post('/refresh', response_model=LoginResponse)
async def refresh_token(refresh_info: RefreshTokenRequest):
    new_access_token: str = await JWTService.refresh_token(refresh_info.refresh_token)
    jwt_token: LoginResponse = LoginResponse(access_token=new_access_token, refresh_token=refresh_info.refresh_token)
    return jwt_token


@router.get('/exist/{user_id}')
async def exist_user_id(user_id: str):
    return UserMapper.exist_user_by_user_id(user_id)