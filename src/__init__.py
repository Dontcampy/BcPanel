import json
import datetime
import socket

import src.api.reg_login as reg_login
import src.api.temp as temp
import src.api.upload as upload
import src.api.sync as sync
import src.api.user as user

from flask import Flask, make_response
from flask_restful import Api
from bson import ObjectId

from src.utils.load_config import config


# 设置socket超时防止假死
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

#
api.add_resource(reg_login.Register, "/api/register")
api.add_resource(reg_login.CheckUsername, "/api/checkusername")
api.add_resource(reg_login.Login, "/api/login")
api.add_resource(temp.GetCard, "/api/getcard")
api.add_resource(temp.GetCompany, "/api/getcompany")
api.add_resource(temp.GetOneCompany, "/api/getonecompany")
api.add_resource(temp.GetVisit, "/api/getvisit")
api.add_resource(temp.AddCard, "/api/addcard")
api.add_resource(temp.AddCompany, "/api/addcompany")
api.add_resource(temp.AddVisit, "/api/addvisit")

api.add_resource(upload.UploadImg, "/api/other/uploadimg")

api.add_resource(user.SetUserInfo, "/user/setuserinfo")

api.add_resource(sync.FirstSync, "/sync/first")
api.add_resource(sync.Compare, "/sync/compare")
api.add_resource(sync.Download, "/sync/download")
api.add_resource(sync.Upload, "/sync/upload")