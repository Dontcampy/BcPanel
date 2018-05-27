import src.dao.user as user
import src.utils.verify as verify

from flask_restful import Resource, reqparse
from flask import request


class UserAdd(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("username")
        parser.add_argument("pwd")
        args = parser.parse_args()

        if verify.verify_t(args["token"]) and user.insert_account(args["username"], args["pwd"]):
            result["success"] = True

        return result


class UserDelete(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("username", action="append")
        args = parser.parse_args()

        if verify.verify_t(args["token"]):
            for item in args["username"]:
                user.del_account(item)
            result["success"] = True
        return result
    

class UserSetPWD(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("username")
        parser.add_argument("pwd")
        args = parser.parse_args()

        if verify.verify_t(args["token"]) and user.set_pwd(args["username"], args["pwd"]):
            result["success"] = True

        return result


class UserSetAdmin(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("username")
        args = parser.parse_args()

        if verify.verify_t(args["token"]) and user.set_admin(args["username"]):
            result["success"] = True
        return result


class UserGetByName(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        username = request.args.get("username")

        if verify.verify_t(token):
            result["data"] = user.select_username(username)
            del result["data"]["pwd"]
            result["success"] = True
        return result


class UserGetFirstPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = user.select_first_page(count)
            result["count"] = user.count()
            result["success"] = True
        return result


class UserGetLastPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = user.select_last_page(count)
            result["count"] = user.count()
            result["success"] = True
        return result


class UserGetPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        _id = request.args.get("_id")
        page = request.args.get("page", type=int)  # 当前页与目标页之差，page > 0 为向后， page < 0 为向前
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = user.select_dir_page(count, page, _id)
            result["count"] = user.count()
            result["success"] = True
        return result


class UserSearch(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        key = request.args.get("key")

        if verify.verify_t(token):
            result["data"] = user.select_fuzzy(key)
            result["success"] = True
        return result
