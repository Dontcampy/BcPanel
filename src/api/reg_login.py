import src.dao.user as user

from flask_restful import Resource, reqparse

from .error import ERROR_0, ERROR_1, Error_Default
from src.utils.verify import get_token, verify_normal, verify_arguments
from src.dao.user import select_username


class Register(Resource):
    def post(self):
        result = {"success": False}
        ver_list = ["username", "pwd"]
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("pwd")
        args = parser.parse_args()

        # 检验关键数据合法性
        if not verify_arguments(ver_list, args):
            result["error"] = ERROR_1
            return result

        # 检验用户是否存在
        if user.select_username(args["username"]):
            result["error"] = ERROR_0
            return result

        # 添加用户并返回token
        if user.insert_account(args["username"], args["pwd"]):
            data = select_username(args["username"])
            del data["pwd"]
            result["success"] = True
            result["token"] = get_token(data["username"])
            result["user"] = data
            return result
        else:
            result["error"] = ERROR_0
            return result


class CheckUsername(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        args = parser.parse_args()

        if args["username"] is None:
            result["error"] = ERROR_1
            return result

        if select_username(args["username"]):
            result["success"] = True
            return result
        else:
            return result


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
