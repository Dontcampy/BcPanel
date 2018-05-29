import ast

import src.dao.company as company
import src.dao.log as log
import src.utils.verify as verify

from flask_restful import Resource, reqparse
from flask import request


class CompanyAdd(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("uuid")
        parser.add_argument("name")
        parser.add_argument("creator")
        parser.add_argument("create_time", type=int)
        parser.add_argument("modifier")
        parser.add_argument("mod_time", type=int)
        parser.add_argument("local_data")
        args = parser.parse_args()

        args["delete"] = False
        args["local_data"] = ast.literal_eval(args["local_data"])
        username = verify.verify_t(args["token"])
        if username and company.insert(args):
            log.insert_insert(args["uuid"], username)
            result["success"] = True
        return result


class CompanyDelete(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("uuid", action="append")
        args = parser.parse_args()

        username = verify.verify_t(args["token"])
        if username:
            for item in args["uuid"]:
                company.delete(item)
                log.insert_delete(item, username)
            result["success"] = True
        return result


class CompanyModify(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("data")
        args = parser.parse_args()

        data = ast.literal_eval(args["data"])
        username = verify.verify_t(args["token"])
        if username and company.update(data["uuid"], data):
            log.insert_modify(data["uuid"], username)
            result["success"] = True
        return result


class CompanyGetByUUID(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        uuid = request.args.get("uuid")

        if verify.verify_t(token):
            result["data"] = company.select_uuid(uuid)
            result["success"] = True
        return result


class CompanyGetFirstPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = company.select_first_page(count)
            result["count"] = company.count()
            result["success"] = True
        return result


class CompanyGetLastPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = company.select_last_page(count)
            result["count"] = company.count()
            result["success"] = True
        return result


class CompanyGetPage(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        _id = request.args.get("_id")
        page = request.args.get("page", type=int)  # 当前页与目标页之差，page > 0 为向后， page < 0 为向前
        count = request.args.get("count", type=int)

        if verify.verify_t(token):
            result["data"] = company.select_dir_page(count, page, _id)
            result["count"] = company.count()
            result["success"] = True
        return result


class CompanySearch(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        key = request.args.get("key")

        if verify.verify_t(token):
            result["data"] = company.select_fuzzy(key)
            result["success"] = True
        return result
