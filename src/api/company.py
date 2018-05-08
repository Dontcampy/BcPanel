# import src.dao.company as company
# import src.dao.visit as visit
# import src.utils.verify as verify
#
# from flask_restful import Resource, reqparse
# from flask import request
#
#
# class GetCount(Resource):
#     def post(self):
#         result = {"success": False}
#         parser = reqparse.RequestParser()
#         parser.add_argument("token")
#         args = parser.parse_args()
#
#         if verify.verify_t(args["token"]):
