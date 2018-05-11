import src.dao.user as user

from flask_restful import Resource, reqparse

from src.utils.verify import get_token, verify_normal, verify_arguments


class Login(Resource):
    def post(self):
        result = {"success": False}
        ver_list = ["username", "pwd"]
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("pwd")
        args = parser.parse_args()

        if not verify_arguments(ver_list, args):
            return result

        if verify_normal(args["username"], args["pwd"]):
            data = user.select_username(args["username"])
            if data["admin"] or data["system"]:
                result["success"] = True
                result["token"] = get_token(data["username"])
                result["user"] = data
                return result

        return result
