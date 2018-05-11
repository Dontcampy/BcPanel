# Database access operations for user
import re

from bson import ObjectId

from src.utils.dbtools import Mongo


def insert_account(username, pwd):
    """
    插入新用户
    :param username: 用户名 str
    :param pwd: 密码 str
    :return: 是否成功 None or ObjectId
    """
    success = None
    mongo = Mongo()
    try:
        data = {"username": username, "pwd": pwd, "admin": False, "vip": True,
                "delete": False, "system": False}
        success = mongo.user.insert(data)
    finally:
        mongo.close()
        return success


def del_account(username):
    """
    :param username: 用户名 str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.remove({"username": username})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def set_pwd(username, pwd):
    """
    修改密码
    :param username: 用户名 str
    :param pwd: 新密码 str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update({"username": username}, {"$set": {"pwd": pwd}})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def set_admin(username):
    """
    修改用户组
    :param username: 用户名 str
    :return: 是否成功 boolean
    """
    success = False
    mongo = Mongo()
    try:
        result = mongo.user.update({"username": username}, {"$set": {"admin": True}})
        success = bool(result["n"])
    finally:
        mongo.close()
        return success


def select_id(_id):
    """
    通过uid查找用户信息
    :param _id: 用户id str
    :return: 用户信息 list<dict> if 不为空 else ()
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.user.find_one({"_id": ObjectId(_id)})
        success = result
    finally:
        mongo.close()
        return success


def select_username(username):
    """
    通过username查找用户信息
    :param username: 用户名 str
    :return: 用户信息 list<dict> if 不为空 else ()
    """
    success = None
    mongo = Mongo()
    try:
        result = mongo.user.find_one({"username": username})
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
        for item in mongo.user.find({"delete": False}).limit(count):
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
        for item in mongo.user.find({"delete": False}).sort("_id", -1).limit(count):
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
            for item in mongo.user.find({"_id": {"$gt": ObjectId(_id)}, "delete": False}).skip(skip_count).limit(count):
                result.insert(0, item)
            success = result
        elif page < 0:
            skip_count = abs(page) * count - 1
            for item in mongo.user.find({"_id": {"$lt": ObjectId(_id)}, "delete": False}).sort("_id", -1).skip(skip_count).limit(count):
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
        for item in mongo.user.find({"_id": {"$gt": ObjectId(_id)}, "delete": False}).skip(skip_count).limit(count):
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
        for item in mongo.user.find({"_id": {"$lt": ObjectId(_id)}, "delete": False}).sort("_id", -1).skip(skip_count).limit(count):
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
        for item in mongo.user.find({"delete": False}).sort("_id", -1).skip(skip_count).limit(count):
            result.append(item)
        success = result
    finally:
        mongo.close()
        return success


def count():
    """
    返回用户数量
    :return: int
    """
    result = 0
    mongo = Mongo()
    try:
        result = mongo.user.find({"delete": False}).count()
    finally:
        mongo.close()
        return result
