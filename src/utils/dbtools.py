from pymongo import MongoClient

from src.utils.load_config import config

class Mongo():
    def __init__(self):
        self.client = MongoClient(config.MONGODB_URI)
        self.db = self.client.businessCard
        self.user = self.db.user
        self.card = self.db.card
        self.company = self.db.company
        self.visit = self.db.visit

    def close(self):
        self.client.close()
