'''
Primary Mongo db class for db actions
- Note:  all Classes EXCEPT BaseMongo are mixin classes
'''
from db.config import settings
from .base_mongo import BaseMongo
from .chatbot_mongo import ChatbotMongo
from .kb_mongo import KbMongo
from .vector import VectorIndex
from .keyword import KeywordIndex

class Mongo(VectorIndex, KeywordIndex, KbMongo, ChatbotMongo, BaseMongo):
    def __init__(self, uri=settings.MONGO_URI):
        super().__init__(uri)
