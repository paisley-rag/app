import os

# from llama_index.core import SimpleDirectoryReader
# from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.core import StorageContext
from dotenv import load_dotenv
import Stemmer

import db.app_logger as log

load_dotenv(dotenv_path='../.env', override=True)

# configs
# db_name = 'keyword1'
# top_k = 5



# general
def get_store(db_name):
    mongo_uri = os.environ["MONGO_URI"]
    store = MongoDocumentStore.from_uri(uri=mongo_uri, db_name=db_name)

    storage_context = StorageContext.from_defaults(
        docstore=store
    )

    return { 'storage_context': storage_context, 'store': store }

def get_retriever(db_name, top_k=None):
    store = get_store(db_name)['store']

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


    log.info(f"keyword.py get_retriever: bm25 retriever returned")
    return bm25_retriever



