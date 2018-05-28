import ast

import src.dao.card as card
import src.utils.verify as verify

from flask_restful import Resource, reqparse
from flask import request


class CardAdd(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("uuid")
        parser.add_argument("name")
        parser.add_argument("company_uuid")
        parser.add_argument("company_name")
        parser.add_argument("creator")
        parser.add_argument("create_time", type=int)
        parser.add_argument("modifier")
        parser.add_argument("mod_time", type=int)
        parser.add_argument("local_data")
        args = parser.parse_args()

        args["delete"] = False
        args["local_data"] = ast.literal_eval(args["local_data"])
        if verify.verify_t(args["token"]) and card.insert(args):
            result["success"] = True
        return result


class CardDelete(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("uuid", action="append")
        args = parser.parse_args()

        if verify.verify_t(args["token"]):
            for item in args["uuid"]:
                card.delete(item)
            result["success"] = True
        return result


class CardModify(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("data")
        args = parser.parse_args()

        data = ast.literal_eval(args["data"])
        if verify.verify_t(args["token"]) and card.update(data["uuid"], data):
            result["success"] = True
        return result


class CardGetByUUID(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        uuid = request.args.get("uuid")

        if verify.verify_t(token):
            result["data"] = card.select_uuid(uuid)
            result["success"] = True
        return result


class CardGetFirstPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = card.select_first_page(count)
            result["count"] = card.count()
            result["success"] = True
        return result


class CardGetLastPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = card.select_last_page(count)
            result["count"] = card.count()
            result["success"] = True
        return result


class CardGetPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        _id = request.args.get("_id")
        page = request.args.get("page", type=int)  # 当前页与目标页之差，page > 0 为向后， page < 0 为向前
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = card.select_dir_page(count, page, _id)
            result["count"] = card.count()
            result["success"] = True
        return result


class CardSearch(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        key = request.args.get("key")

        if verify.verify_t(token):
            result["data"] = card.select_fuzzy(key)
            result["success"] = True
        return result
