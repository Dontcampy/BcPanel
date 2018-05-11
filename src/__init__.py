import json
import datetime
import socket

import src.api.reg_login as reg_login
import src.api.user as user
import src.api.card as card
import src.api.company as company
import src.api.visit as visit

from flask import Flask, make_response
from flask_restful import Api
from bson import ObjectId

from src.utils.load_config import config


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

api.add_resource(card.Add, "/card/add")
api.add_resource(card.Delete, "/card/delete")
api.add_resource(card.Modify, "/card/modify")
api.add_resource(card.GetFirstPage, "/card/getfirstpage")
api.add_resource(card.GetLastPage, "/card/getlastpage")
api.add_resource(card.GetPage, "/card/getpage")
api.add_resource(card.Search, "/card/search")

api.add_resource(company.Add, "/company/add")
api.add_resource(company.Delete, "/company/delete")
api.add_resource(company.Modify, "/company/modify")
api.add_resource(company.GetFirstPage, "/company/getfirstpage")
api.add_resource(company.GetLastPage, "/company/getlastpage")
api.add_resource(company.GetPage, "/company/getpage")
api.add_resource(company.Search, "/company/search")

api.add_resource(visit.Add, "/card/add")
api.add_resource(visit.Delete, "/card/delete")
api.add_resource(visit.Modify, "/card/modify")
api.add_resource(visit.GetFirstPage, "/card/getfirstpage")
api.add_resource(visit.GetLastPage, "/card/getlastpage")
api.add_resource(visit.GetPage, "/card/getpage")
api.add_resource(visit.Search, "/card/search")

api.add_resource(user.Add, "/user/add")
api.add_resource(user.Delete, "/user/delete")
api.add_resource(user.SetPWD, "/user/setpwd")
api.add_resource(user.SetAdmin, "/user/setadmin")
api.add_resource(user.GetFirstPage, "/user/getfirstpage")
api.add_resource(user.GetLastPage, "/user/getlastpage")
api.add_resource(user.GetPage, "/user/getpage")
api.add_resource(user.Search, "/user/search")
