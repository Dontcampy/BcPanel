import ast

import src.dao.visit as visit
import src.utils.verify as verify

from flask_restful import Resource, reqparse
from flask import request


class VisitAdd(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("uuid")
        parser.add_argument("owner_uuid")
        parser.add_argument("creator")
        parser.add_argument("create_time", type=int)
        parser.add_argument("modifier")
        parser.add_argument("mod_time", type=int)
        parser.add_argument("local_data")
        args = parser.parse_args()

        args["delete"] = False
        if verify.verify_t(args["token"]) and visit.insert(args):
            result["success"] = True
        return result


class VisitDelete(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("uuid", action="append")
        args = parser.parse_args()

        if verify.verify_t(args["token"]):
            for item in args["uuid"]:
                visit.delete(item)
            result["success"] = True
        return result


class VisitModify(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("data")
        args = parser.parse_args()

        data = ast.literal_eval(args["data"])
        if verify.verify_t(args["token"]) and visit.update(data["uuid"], data):
            result["success"] = True
        return result


class VisitGetByUUID(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        uuid = request.args.get("uuid")

        if verify.verify_t(token):
            result["data"] = visit.select_uuid(uuid)
            result["success"] = True
        return result


class VisitGetFirstPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = visit.select_first_page(count)
            result["count"] = visit.count()
            result["success"] = True
        return result


class VisitGetLastPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = visit.select_last_page(count)
            result["count"] = visit.count()
            result["success"] = True
        return result


class VisitGetPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        _id = request.args.get("_id")
        page = request.args.get("page", type=int)  # 当前页与目标页之差，page > 0 为向后， page < 0 为向前
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = visit.select_dir_page(count, page, _id)
            result["count"] = visit.count()
            result["success"] = True
        return result


class VisitSearch(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        key = request.args.get("key")

        if verify.verify_t(token):
            result["data"] = visit.select_fuzzy(key)
            result["success"] = True
        return result
