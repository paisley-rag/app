'''
Mixin class for chatbot class db access
'''
import logging
from db.db.base_mongo import BaseMongo
from db.config import settings

class ChatbotMongo(BaseMongo):
    def set_chatbot_db(self, chatbot_db=settings.CONFIG_DB, chatbot_col=settings.CONFIG_PIPELINE_COL):
        self._chatbot_db = self._client[chatbot_db][chatbot_col]

    # CRUD methods for chatbot class
    def get_one_chatbot(self, get_id):
        result = self._chatbot_db.find_one(
            {"id": get_id},
            {'_id': 0}
        )
        return result

    def get_all_chatbots(self):
        results = self._chatbot_db.find(
            {},
            { '_id': 0 }
        )
        results = list(results)
        return results

    def chatbot_name_taken(self, name):
        result = self._chatbot_db.find_one(
            { "name": name },
            { '_id': 0 }
        )
        return result

    def delete_chatbot(self, get_id):
        result = self._chatbot_db.delete_one(
            { "id": get_id }
        )
        return result

    def insert_chatbot(self, doc):
        result = self._chatbot_db.insert_one(doc)
        return result

    def add_id_to_chatbot_config(self, name, inserted_id):
        result = self._chatbot_db.update_one(
            { "name": name },
            { "$set": { "id": inserted_id } }
        )
        return result

    def update_chatbot(self, get_id, new_config):
        print('starting update_chatbot')
        old_config = self.get_one_chatbot(get_id)
        print('got old_config', old_config)
        updates = self.compare_configs(old_config, new_config)
        print('compared configs', updates)

        if updates:
            self._chatbot_db.update_one(
                { "id": get_id },
                { "$set": updates }
            )
            print('made updates')

        print('about to return one chatbot', get_id)
        return self.get_one_chatbot(get_id)

    def compare_configs(self, old_config, new_config):
        updates = {}
        for key in new_config:
            if new_config[key] != old_config[key]:
                updates[key] = new_config[key]
        return updates

# used in chatbot class
    def nodes_in_keyword(self, kb_id):
        results = self._client[kb_id]['docstore/ref_doc_info'].find(
            {},
            { '_id': 0 }
        )
        results = list(results)
        return len(results)
