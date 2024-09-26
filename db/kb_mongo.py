'''
Mixin class for kb class db access
'''

import db.app_logger as log
from db.db.base_mongo import BaseMongo
from db.config import settings

class KbMongo(BaseMongo):
    def set_kb_db(
        self,
        kb_db=settings.CONFIG_DB,
        kb_col=settings.CONFIG_KB_COL
    ):
        self._kb_db = self._client[kb_db][kb_col]

    # CRUD methods for kb class
    def get_knowledge_bases(self):
        result = self._kb_db.find({}, {'_id': 0})
        return list(result)

    def knowledge_base_name_taken(self, kb_name):
        result = self._kb_db.find_one({'kb_name': kb_name}, {'_id': 0})
        return result

    def get_knowledge_base(self, get_id):
        result = self._kb_db.find_one({'id': get_id}, {'_id': 0})
        return result

    def insert_knowledge_base(self, kb_config):
        result = self._kb_db.insert_one(kb_config)
        return result

    async def add_file_metadata_to_kb(self, kb_name, file_metadata):
        log.info(f"add_file_metadata_to_kb: start {kb_name}")
        result = self._kb_db.update_one(
            { "kb_name": kb_name },
            { "$push": { "files": file_metadata } }
        )
        log.info(f"add_file_metadata_to_kb: {result}")
        return result

    def file_exists(self, get_id, file):
        kb = self.get_knowledge_base(get_id)
        if kb:
            for f in kb["files"]:
                if (
                    f["file_name"] == file.filename and
                    f["size"] == file.size and
                    f["content_type"] == file.headers["content-type"]
                    ):
                    return True
        return False


    def add_id_to_kb_config(self, kb_name, kb_id):
        result = self._kb_db.update_one(
            { "kb_name": kb_name },
            { "$set": { "id": kb_id } }
        )
        log.info(f"add_id_to_kb_config: {result}")
        return result

    def get_kb_id(self, kb_name):
        result = self._kb_db.find_one(
            {"kb_name": kb_name}
        )
        log.info("result id string:", str(result["_id"]))
        if result:
            return str(result["_id"])

        return None

    def delete_knowledge_base(self, get_id):
        kb_result = self._kb_db.delete_one({"id": get_id})
        self.remove_kb_from_pipeline(get_id)
        self.drop_db(get_id)
        return kb_result

    def remove_kb_from_pipeline(self, kb_id):
        result = self._kb_db.update_many(
            {},
            { "$pull": { "knowledge_bases": kb_id } }
        )
        log.info(f"remove_kb_from_pipeline: {result}")
        return result
