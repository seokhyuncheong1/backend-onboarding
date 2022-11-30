from pydantic import (
    BaseModel,
    Field
)
from typing import Union

class TestResponse(BaseModel):
    id: int = Field(title='')
    message: Union[str, None] = Field(title='')
