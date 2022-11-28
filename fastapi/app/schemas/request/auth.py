from pydantic import BaseModel


class SignupRequest(BaseModel):
    user_id: str
    user_password: str
    user_password_confirm: str


class LoginRequest(BaseModel):
    user_id: str
    user_password: str