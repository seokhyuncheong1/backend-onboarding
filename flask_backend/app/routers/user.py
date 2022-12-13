from flask import request, Response, jsonify, make_response
from flask_restx import Resource, Namespace

from app.services.user import UserService


UserApi = Namespace("User")


@UserApi.route("/login")
class Login(Resource):
    def post(self):
        user_id: str = request.json["user_id"]
        user_password: str = request.json["user_password"]

        json_token = UserService().login_user(user_id, user_password)

        response: Response = make_response(jsonify(json_token))
        response.set_cookie("access_token", json_token["access_token"])
        response.set_cookie("refresh_token", json_token["refresh_token"])

        return response
