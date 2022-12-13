from flask_restx import Api
from .todo import TodoApi
from .user import UserApi

api = Api()

api_prefix = "/api/v1"
api.add_namespace(TodoApi, f'{api_prefix}/todo')
api.add_namespace(UserApi, f'{api_prefix}/auth')
