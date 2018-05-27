import json
import datetime
import socket

import src.api.reg_login as reg_login

from flask import Flask, make_response
from flask_restful import Api
from bson import ObjectId

from src.utils.load_config import config
from src.api import *


# 设置socket超时防止假死, 仅调试阶段使用
socket.setdefaulttimeout(10)

app = Flask(__name__)
api = Api(app)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return str(o)
    elif isinstance(o, ObjectId):
        return str(o)


# 跨域请求
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, default=myconverter), code)
    resp.headers.extend(headers or {'Access-Control-Allow-Origin': '*'})
    return resp


api.add_resource(reg_login.Login, "/login")

api.add_resource(CardAdd, "/card/add")
api.add_resource(CardDelete, "/card/delete")
api.add_resource(CardModify, "/card/modify")
api.add_resource(CardGetByUUID, "/card/getbyuuid")
api.add_resource(CardGetFirstPage, "/card/getfirstpage")
api.add_resource(CardGetLastPage, "/card/getlastpage")
api.add_resource(CardGetPage, "/card/getpage")
api.add_resource(CardSearch, "/card/search")

api.add_resource(CompanyAdd, "/company/add")
api.add_resource(CompanyDelete, "/company/delete")
api.add_resource(CompanyModify, "/company/modify")
api.add_resource(CompanyGetByUUID, "/company/getbyuuid")
api.add_resource(CompanyGetFirstPage, "/company/getfirstpage")
api.add_resource(CompanyGetLastPage, "/company/getlastpage")
api.add_resource(CompanyGetPage, "/company/getpage")
api.add_resource(CompanySearch, "/company/search")

api.add_resource(VisitAdd, "/visit/add")
api.add_resource(VisitDelete, "/visit/delete")
api.add_resource(VisitModify, "/visit/modify")
api.add_resource(VisitGetByUUID, "/visit/getbyuuid")
api.add_resource(VisitGetFirstPage, "/visit/getfirstpage")
api.add_resource(VisitGetLastPage, "/visit/getlastpage")
api.add_resource(VisitGetPage, "/visit/getpage")
api.add_resource(VisitSearch, "/visit/search")

api.add_resource(UserAdd, "/user/add")
api.add_resource(UserDelete, "/user/delete")
api.add_resource(UserSetPWD, "/user/setpwd")
api.add_resource(UserSetAdmin, "/user/setadmin")
api.add_resource(UserGetByName, "/user/getbyname")
api.add_resource(UserGetFirstPage, "/user/getfirstpage")
api.add_resource(UserGetLastPage, "/user/getlastpage")
api.add_resource(UserGetPage, "/user/getpage")
api.add_resource(UserSearch, "/user/search")
