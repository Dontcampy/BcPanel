import re
import traceback

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
        if "token" in data:
            del data["token"]
        success = mongo.visit.insert(data)
    except Exception as e:
        traceback.print_exc()
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
        result = mongo.visit.update_one({"uuid": uuid}, {"$set": {"delete": True}})
        success = bool(True)
    except Exception as e:
        traceback.print_exc()
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
        if "_id" in new_data:
            del new_data["id"]
        result = mongo.visit.update_one({"uuid": uuid}, {"$set": new_data})
        success = bool(True)
    except Exception as e:
        traceback.print_exc()
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
        success = result
    except Exception as e:
        traceback.print_exc()
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
            result.append(item)
        success = result
    except Exception as e:
        traceback.print_exc()
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
            result.append(item)
        success = result
    except Exception as e:
        traceback.print_exc()
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
    except Exception as e:
        traceback.print_exc()
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
    except Exception as e:
        traceback.print_exc()
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
    except Exception as e:
        traceback.print_exc()
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
    except Exception as e:
        traceback.print_exc()
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
    except Exception as e:
        traceback.print_exc()
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
    except Exception as e:
        traceback.print_exc()
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
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return result


def select_fuzzy(key):
    """
    根据关键字进行模糊查询
    :param key: str 关键字
    :return:
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.company.find({"$or": [{"creator": re.compile(key)}]}).sort("_id", -1):
            result.append(item)
        success = result
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success
