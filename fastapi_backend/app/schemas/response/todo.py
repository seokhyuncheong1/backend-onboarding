from pydantic import BaseModel
from datetime import datetime


class TodoDTO(BaseModel):
    title: str
    detail: str | None
    user_id: str
    created_at: datetime