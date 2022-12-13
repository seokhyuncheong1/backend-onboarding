from pydantic import BaseModel


class TodoRequest(BaseModel):
    title: str
    detail: str | None

    def __to_dict__(self):
        return {
            "title": self.title,
            "detail": self.detail
        }