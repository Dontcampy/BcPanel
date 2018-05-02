import os

import werkzeug.datastructures

from flask_restful import Resource, reqparse

from .error import ERROR_4


class UploadImg(Resource):
    def post(self):
        result = {"success": False}
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("filename")

        args = parser.parse_args()

        # 将图片保存至images文件夹
        try:
            file = args["image"]
            if file is None or bool(file.filename) is False:
                result["error"] = "上传文件不可为空"
                return result
            file.save(os.path.join('/usr/share/nginx/html/images', args["filename"]))
            image_url = 'images/' + args["filename"]
            result["success"] = True
            result["imgURL"] = image_url
        except Exception as e:
            print(e)
            result["error"] = ERROR_4
            return result
        return result
