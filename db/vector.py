'''
Mixin class for vector search
'''
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

from db.db.base_mongo import BaseMongo
import db.app_logger as log
from db.config import settings

log.info(f"vector.py: using environment '{settings.ENVIRONMENT}'")

class VectorIndex(BaseMongo):

    # for kb_class
    def get_vector_storage_context(self, db_name):
        if settings.ENVIRONMENT in ('mongoatlas', 'local'):
            store = self.get_mongo_atlas(db_name)
        else:
            store = self.get_prod(db_name)

        storage_context = StorageContext.from_defaults(vector_store=store)
        return storage_context

    # for chatbot_class
    def get_vector_retriever(self, db_name, top_k=None):
        if settings.ENVIRONMENT in ('mongoatlas', 'local'):
            log.info('vector.py get_retriever - mongoAtlas', db_name)
            store = self.get_mongo_atlas(db_name)
        else:
            log.info('vector.py get_retriever - production', db_name)
            store = self.get_prod(db_name)

        return self._get_retriever(store, top_k)

    def get_prod(self, db_name):
        '''
        for DocDB (i.e., prod)
        '''
        store = AWSDocDbVectorStore(
            self._client,
            db_name=db_name,
            collection_name=settings.VECTOR_COLLECTION_NAME
        )
        log.info(f"vector.py : AWSDocDb vector store returned for [{db_name}]")
        return store

    def get_mongo_atlas(self, db_name):
        '''
        for MongoAtlas (i.e., local)
        '''
        store = MongoDBAtlasVectorSearch(
            self._client,
            db_name=db_name,
            collection_name=settings.VECTOR_COLLECTION_NAME
        )
        log.info(f"vector.py : MongoDBAtlas vector store returned for [{db_name}]")
        return store

    def _get_retriever(self, store, top_k):
        log.info('vector.py _get_retriever')
        storage_context = StorageContext.from_defaults(vector_store=store)

        vector_index = VectorStoreIndex.from_vector_store(
            vector_store=store,
            storage_context=storage_context
        )

        if top_k:
            vector_retriever = vector_index.as_retriever(similarity_top_k=top_k)
        else:
            vector_retriever = vector_index.as_retriever()

        log.info("vector.py : vector retriever returned")

        return vector_retriever
