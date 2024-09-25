'''
Mixin class for keyword search
'''
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.core import StorageContext
import Stemmer

from db.db.base_mongo import BaseMongo
import db.app_logger as log

class KeywordIndex(BaseMongo):

    # for kb_class
    def get_keyword_store(self, kb_id):
        return self._get_store(kb_id)['store']

    # for chatbot_class
    def get_keyword_retriever(self, db_name, top_k=None):
        store = self._get_store(db_name)['store']

        if top_k:
            bm25_retriever = BM25Retriever.from_defaults(
                docstore=store,
                similarity_top_k=top_k,
                stemmer=Stemmer.Stemmer('english'),
                language='english',
            )
        else:
            bm25_retriever = BM25Retriever.from_defaults(
                docstore=store,
                stemmer=Stemmer.Stemmer('english'),
                language='english',
            )


        log.info("keyword.py get_retriever: bm25 retriever returned")
        return bm25_retriever

    def _get_store(self, db_name):
        store = MongoDocumentStore.from_uri(uri=self._uri, db_name=db_name)

        storage_context = StorageContext.from_defaults(
            docstore=store
        )

        return { 'storage_context': storage_context, 'store': store }
