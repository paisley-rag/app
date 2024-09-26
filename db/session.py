'''
Create a (mongo) db instance for app
'''
from db.config import settings
from .mongo import Mongo

def get_db():
    db = Mongo(settings.MONGO_URI)
    db.set_chatbot_db(settings.CONFIG_DB, settings.CONFIG_PIPELINE_COL)
    db.set_kb_db(settings.CONFIG_DB, settings.CONFIG_KB_COL)
    try:
        yield db
    finally:
        db.close()
