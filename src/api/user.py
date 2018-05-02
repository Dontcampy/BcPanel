import src.dao.user as user
import src.utils.verify as verify

from flask_restful import Resource, reqparse

class SetUserInfo(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument("token")
        parser.add_argument("avatar")
        parser.add_argument("section")
        parser.add_argument("position")
        args = parser.parse_args()

        username = verify.verify_t(args["token"])

        if username and user.set_info(username, args["avatar"], args["section"], args["position"]):
            result["success"] = True

        return result