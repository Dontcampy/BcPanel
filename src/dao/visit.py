from bson import ObjectId

from src.utils.dbtools import Mongo


def insert(data):
    """
    插入
    :param data: 数据 dict
    :return: None or ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        success = mongo.visit.insert(data)
    finally:
        mongo.close()
        return success


def delete(uuid):
    """
    删除
    :param uuid: id str
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.visit.remove({"uuid": uuid})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def update(uuid, new_data):
    """
    更新
    :param uuid: id str
    :param new_data: 新数据 dict
    :return: boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.visit.update_one({"uuid": uuid}, {"$set": new_data}, upsert=True)
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def select_uuid(uuid):
    """
    通过id查询
    :param uuid: str
    :return: None or dict
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.visit.find_one({"uuid": uuid})
        del result["_id"]
        success = result
    finally:
        mongo.close()
        return success


def select_owner(owner_uuid):
    """
    owner_uuid
    :param owner_uuid: str
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.visit.find({"owner_uuid": owner_uuid}).sort('_id', -1):
            del item["_id"]
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def select_all():
    """
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.visit.find():
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
        for item in mongo.visit.find({"create_time": {"$gt": timestamp}}, {"_id":0, "uuid": 1}):
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
        for item in mongo.visit.find({"delete": False}).limit(count):
            result.insert(0, item)
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
        for item in mongo.visit.find({"delete": False}).sort("_id", -1).limit(count):
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
            skip_count = (page - 1) * count
            for item in mongo.visit.find({"_id": {"$gt": ObjectId(_id)}, "delete": False}).skip(skip_count).limit(count):
                result.insert(0, item)
            success = result
        elif page < 0:
            skip_count = abs(page) * count - 1
            for item in mongo.visit.find({"_id": {"$lt": ObjectId(_id)}, "delete": False}).sort("_id", -1).skip(skip_count).limit(count):
                result.append(item)
            success = result
    finally:
        mongo.close()
        return success


def select_pre_page(count, page, _id):
    """
    获取前页数据
    :param count: 每页数量
    :param page: 当前页与目标页之差，应该大于0
    :param _id: 当前页第一条数据的_id
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        skip_count = (page - 1) * count
        for item in mongo.visit.find({"_id": {"$gt": ObjectId(_id)}, "delete": False}).skip(skip_count).limit(count):
            result.insert(0, item)
        success = result
    finally:
        mongo.close()
        return success


def select_next_page(count, page, _id):
    """
    获取后页数据
    :param count: 每页数量
    :param page: 当前页与目标页之差，应该小于0
    :param _id: 当前页第一条数据的_id
    :return: list or None
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        skip_count = abs(page) * count - 1
        for item in mongo.visit.find({"_id": {"$lt": ObjectId(_id)}, "delete": False}).sort("_id", -1).skip(skip_count).limit(count):
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
        for item in mongo.visit.find({"delete": False}).sort("_id", -1).skip(skip_count).limit(count):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def count():
    """
    返回拜访记录数量
    :return: int
    """
    result = 0
    mongo = Mongo()
    try:
        result = mongo.visit.find({"delete": False}).count()
    finally:
        mongo.close()
        return result
