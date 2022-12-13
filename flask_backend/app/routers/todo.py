from flask import request
from flask_restx import Resource, Namespace
from typing import List

from app.middlewares.jwt import login_required
from app.common.services.jwt import JWTService
from app.services.todo import TodoService

TodoApi = Namespace("Todo")


@TodoApi.route("")
class TodoPost(Resource):
    @login_required
    def get(self):
        user_id: str = JWTService.verify_token(request.cookies.get("access_token"))
        todo_list = TodoService().get_todos(user_id)

        return {
            "todo_list": todo_list
        }

    def post(self):
        print(request.json)
        todo_title: str = request.json["title"]
        todo_detail: str | None = request.json["detail"]

        return {
            "title": todo_title,
            "detail": todo_detail
        }
