import src.dao.log as log
import src.utils.verify as verify

from flask_restful import Resource
from flask import request


class LogGetByUUID(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        uuid = request.args.get("uuid")

        if verify.verify_t(token):
            result["data"] = log.select_uuid(uuid)
            result["success"] = True
        return result


class LogGetByName(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")
        username = request.args.get("username")

        if verify.verify_t(token):
            result["data"] = log.select_username(username)
            result["success"] = True
        return result
