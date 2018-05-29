import traceback

from src.utils.useful import get_13ts
from src.utils.dbtools import Mongo


def insert_login(username):
    """
    登录事件log
    :param username: 用户名
    :return: ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        log_data = {"uuid": None, "username": username, "date": get_13ts(), "oper": "login"}
        success = mongo.log.insert_one(log_data)
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success


def insert_insert(uuid, username):
    """
    添加事件log记录
    :param uuid: uuid
    :param username: 用户名
    :return: ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        log_data = {"uuid": uuid, "username": username, "date": get_13ts(), "oper": "insert"}
        success = mongo.log.insert_one(log_data)
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success


def insert_delete(uuid, username):
    """
    删除事件log记录
    :param uuid: uuid
    :param username: 用户名
    :return: ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        log_data = {"uuid": uuid, "username": username, "date": get_13ts(), "oper": "delete"}
        success = mongo.log.insert_one(log_data)
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success


def insert_modify(uuid, username):
    """
    修改事件log记录
    :param uuid: uuid
    :param username: 用户名
    :return: ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        log_data = {"uuid": uuid, "username": username, "date": get_13ts(), "oper": "modify"}
        success = mongo.log.insert_one(log_data)
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success


def select_login():
    """
    查询所有登录记录
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.log.find({"oper": "login"}).sort('_id', -1):
            result.append(item)
        success = result
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success


def select_uuid(uuid):
    """
    通过uuid查询记录
    :param uuid: uuid
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.log.find({"uuid": uuid}).sort('_id', -1):
            result.append(item)
        success = result
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success


def select_username(username):
    """
    通过username查询记录
    :param username: username
    :return: None or list
    """
    success = None
    result = []
    mongo = Mongo()
    try:
        for item in mongo.log.find({"username": username}).sort('_id', -1):
            result.append(item)
        success = result
    except Exception as e:
        traceback.print_exc()
    finally:
        mongo.close()
        return success
