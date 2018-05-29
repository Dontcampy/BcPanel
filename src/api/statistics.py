import src.dao.card as card
import src.dao.company as company
import src.dao.visit as visit
import src.utils.verify as verify

from flask_restful import Resource
from flask import request


class StatGetAll(Resource):
    def get(self):
        result = {"success": False}
        token = request.args.get("token")

        print(verify.verify_t(token))
        if verify.verify_t(token):
            result["cards"] = card.count()
            result["company"] = company.count()
            result["visit"] = visit.count()
            result["success"] = True
        return result
