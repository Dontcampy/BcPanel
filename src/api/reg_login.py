import src.dao.user as user

from flask_restful import Resource, reqparse

from .error import ERROR_0, ERROR_1, Error_Default
from src.utils.verify import get_token, verify_normal, verify_arguments
from src.dao.user import select_username


class Login(Resource):
    def post(self):
        result = {"success": False}
        ver_list = ["username", "pwd"]
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("pwd")
        args = parser.parse_args()

        if not verify_arguments(ver_list, args):
            result["error"] = ERROR_1
            return result

        if verify_normal(args["username"], args["pwd"]):
            data = select_username(args["username"])
            del data["pwd"]

            result["success"] = True
            result["token"] = get_token(data["username"])
            result["user"] = data
            return result
        else:
            result["error"] = Error_Default
            return result
