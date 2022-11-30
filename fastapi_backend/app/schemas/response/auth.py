from pydantic import (
    BaseModel,
    Field
)


class LoginResponse(BaseModel):
    access_token: str = Field(title='접근을 위한 JWT 토큰')
    refresh_token: str = Field(title='토큰 재발급을 위한 JWT 토큰')