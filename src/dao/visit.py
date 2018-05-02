from src.utils.dbtools import Mongo

# data = {"_id": ObjectId(),
#         "uuid": "", //客户端分配的uuid
#         "owner_uuid": "uuid", //创建这条拜访记录的公司的uuid
#         "company": "", //拜访公司名
#         "aim": "", // 目的
#         "creator": "",
#         "create_time": time.time(),
#         "modifier": "",
#         "mod_time": time.time()}

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
