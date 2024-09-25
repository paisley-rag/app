from .mongo import Mongo
from db.config import settings

def get_db():
    try:
        db = Mongo(settings.MONGO_URI)
        db.set_chatbot_db(settings.CONFIG_DB, settings.CONFIG_PIPELINE_COL)
        db.set_kb_db(settings.CONFIG_DB, settings.CONFIG_KB_COL)
        yield db
    finally:
        db.close()


# def get_chatbot_db():
#     try:
#         chatbot_db = ChatbotMongo(MONGO_URI, CONFIG_DB, CONFIG_PIPELINE_COL)
#         chatbot_db.connect()
#         yield chatbot_db
#     finally:
#         chatbot_db.close()
# 
# 
# def get_kb_db():
#     try:
#         kb_db = KbMongo(MONGO_URI, CONFIG_DB, CONFIG_KB_COL)
#         kb_db.connect()
#         yield kb_db
#     finally:
#         kb_db.close()
# 
# 
# def get_vector_index():
#     return VectorIndex(Mongo(MONGO_URI))
# 
# def get_keyword_index():
#     return KeywordIndex(Mongo(MONGO_URI))
