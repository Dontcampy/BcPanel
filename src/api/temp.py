import src.dao.card as card
import src.dao.company as company
import src.dao.visit as visit
import src.utils.verify as verify

from flask_restful import Resource, reqparse
from flask import request

from .error import ERROR_0, ERROR_1


class GetCard(Resource):
    def get(self):
        result = {"success": False}
        # uuid = request.args.get("uuid")
        #
        # if not uuid:
        #     result["error"] = ERROR_1
        #     return result

        result["data"] = card.select_all()
        result["success"] = True
        return result


class AddCard(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
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

        card.insert(args)

        result["success"] = True
        return result


class GetCompany(Resource):
    def get(self):
        result = {"success": False}
        # uuid = request.args.get("uuid")
        #
        # if not uuid:
        #     result["error"] = ERROR_1
        #     return result

        result["data"] = company.select_all()
        result["success"] = True
        return result


class GetOneCompany(Resource):
    def get(self):
        result = {"success": False}
        uuid = request.args.get("uuid")

        if not uuid:
            result["error"] = ERROR_1
            return result

        result["data"] = company.select_uuid(uuid)
        result["success"] = True
        return result


class AddCompany(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("uuid")
        parser.add_argument("name")
        parser.add_argument("creator")
        parser.add_argument("create_time", type=int)
        parser.add_argument("modifier")
        parser.add_argument("mod_time", type=int)
        parser.add_argument("local_data")
        args = parser.parse_args()

        company.insert(args)

        result["success"] = True
        return result


class GetVisit(Resource):
    def get(self):
        result = {"success": False}
        owner_uuid = request.args.get("owner_uuid")

        if not owner_uuid:
            result["error"] = ERROR_1
            return result

        result["data"] = visit.select_owner(owner_uuid)
        result["success"] = True
        return result


class AddVisit(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("uuid")
        parser.add_argument("owner_uuid")
        parser.add_argument("creator")
        parser.add_argument("create_time", type=int)
        parser.add_argument("modifier")
        parser.add_argument("mod_time", type=int)
        parser.add_argument("local_data")
        args = parser.parse_args()

        visit.insert(args)

        result["success"] = True
        return result
