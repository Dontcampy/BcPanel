from src.utils.dbtools import Mongo
from bson import ObjectId


def insert(data):
    """
    插入名片
    :param data: 名片数据 dict
    :return: None or ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        success = mongo.card.insert(data)
    finally:
        mongo.close()
        return success


def delete(uuid):
    """
    删除名片
    :param uuid: 名片id str
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.card.remove({"uuid": uuid})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def update(uuid, new_data):
    """
    更新名片
    :param uuid: 名片id str
    :param new_data: 新数据 dict
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.card.update_one({"uuid": uuid}, {"$set": new_data}, upsert=True)
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def select_uuid(uuid):
    """
    通过uuid查询
    :param uuid: str
    :return: None or dict
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.card.find_one({"uuid": uuid})
        del result["_id"]
        success = result
    finally:
        mongo.close()
        return success


def select_name(name):
    """
    通过name查询
    :param name: str
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find({"name": name}):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_company(company):
    """
    通过company_name查询
    :param name: str
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find({"company_name": company}):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_all():
    """
    查询
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find():
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_newest(timestamp):
    """
    将上次用户同步后的新数据uuid返回
    :param timestamp: 时间戳timestamp
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find({"create_time": {"$gt": timestamp}}, {"_id":0, "uuid": 1}):
            result.append(item["uuid"])
        success = result
    finally:
        mongo.close()
        return success


def select_last_page(count):
    """
    获取最后一页数据
    :param count: int 每页条数
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find({"delete": False}).limit(count).sort("_id", -1):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_first_page(count):
    """
    获取第一页数据
    :param count: int 每页条数
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.card.find({"delete": False}).sort("_id", -1).limit(count):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_dir_page(count, page, _id):
    """
    根据page值获取前后页数据
    :param count: 每页数量
    :param page: 当前页与目标页之差，page > 0 为向后， page < 0 为向前
    :param _id: 当前页第一条数据的_id
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        if page > 0:
            condition = "$lt"
            skip_count = page * count - 1
        elif page < 0:
            condition = "$gt"
            skip_count = (abs(page) - 1) * count
        else:
            return None
        for item in mongo.card.find({"_id": {condition: ObjectId(_id)}, "delete": False}).sort("_id", -1).skip(skip_count).limit(count):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_pre_page(count, page, _id):
    """
    获取前页数据
    :param count: 每页数量
    :param page: 当前页与目标页之差
    :param _id: 当前页第一条数据的_id
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        skip_count = (abs(page) - 1) * count
        for item in mongo.card.find({"_id": {"$gt": ObjectId(_id)}, "delete": False}).sort("_id", -1).skip(skip_count).limit(count):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_next_page(count, page, _id):
    """
    获取后页数据
    :param count: 每页数量
    :param page: 当前页与目标页之差
    :param _id: 当前页第一条数据的_id
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        skip_count = page * count - 1
        for item in mongo.card.find({"_id": {"$lt": ObjectId(_id)}, "delete": False}).sort("_id", -1).skip(skip_count).limit(count):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_page(count, page):
    """
    直接获取目标页数据，由于mongodb的skip特性，数据量过大的情况下性能十分堪忧，谨慎使用
    :param count: 每页数量
    :param page: 目标页数（非差值）
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        skip_count = (page - 1) * count
        for item in mongo.card.find({"delete": False}).sort("_id", -1).skip(skip_count).limit(count):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def count():
    """
    返回名片数量
    :return: int
    """
    result = 0
    mongo = Mongo()
    try:
        result = mongo.card.find({"delete": False}).count()
    finally:
        mongo.close()
        return result
