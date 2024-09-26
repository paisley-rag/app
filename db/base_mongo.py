'''
Base utility class for mongo
- extended by chatbot_mongo and kb_mongo
'''
import pymongo
# from motor.motor_asyncio import AsyncIOMotorClient
class MongoError(Exception):
    pass

class BaseMongo:
    def __init__(self, uri):
        self._uri = uri
        self._client = pymongo.MongoClient(self._uri)
        # self._client = AsyncIOMotorClient(self._uri)

    # getter methods
    def uri(self):
        return self._uri

    def client(self):
        return self._client

    # connection methods

    def close(self):
        self._client.close()

    def drop_db(self, db_name=None):
        if db_name:
            self._client.drop_database(db_name)
        else:
            raise MongoError('drop_db method: no db_name provided or previously defined')
