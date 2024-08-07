import os

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
import pymongo

import db.app_logger as log

load_dotenv(override=True)

# configs
# top_k = 5
environment = os.environ["ENVIRONMENT"]

log.info(f"vector.py: using environment '{environment}'")


# "interface" functions

def get_retriever(db_name, top_k):
    if environment == 'mongoatlas':
        return read_mongoAtlas(db_name, top_k)
    else:
        return read_prod(db_name, top_k)




# docdb functions

COLLECTION_NAME = 'vector_index'
MONGO_URI = os.environ["MONGO_URI"]


# def write_prod(db_name, file_path):
#     if os.path.isdir(file_path):
#         documents = SimpleDirectoryReader(file_path).load_data()
#     else:
#         documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
# 
#     mongodb_client = pymongo.MongoClient(MONGO_URI)
#     store = AWSDocDbVectorStore(
#         mongodb_client,
#         db_name=db_name,
#         collection_name=COLLECTION_NAME
#     )
#     storage_context = StorageContext.from_defaults(vector_store=store)
# 
#     VectorStoreIndex.from_documents(
#         documents, storage_context=storage_context
#     )
# 
#     mongodb_client.close()
#     log.info(f"vector.py write_prod: {file_path} written to mongo {db_name}/{COLLECTION_NAME}")


def read_prod(db_name, top_k):
    mongodb_client = pymongo.MongoClient(MONGO_URI)
    store = AWSDocDbVectorStore(
        mongodb_client,
        db_name=db_name,
        collection_name=COLLECTION_NAME
    )
    storage_context = StorageContext.from_defaults(vector_store=store)

    vector_index = VectorStoreIndex.from_vector_store(
        vector_store=store,
        storage_context=storage_context
    )

    vector_retriever = vector_index.as_retriever(similarity_top_k=top_k)

    # mongodb_client.close()
    log.info(f"vector.py read_prod: vector retriever returned from mongo {db_name}/{COLLECTION_NAME}")
    return vector_retriever

# MongoAtlas functions

def read_mongoAtlas(db_name, top_k):
    mongodb_client = pymongo.MongoClient(MONGO_URI)
    store = MongoDBAtlasVectorSearch(
        mongodb_client,
        db_name=db_name,
        collection_name=COLLECTION_NAME
    )
    storage_context = StorageContext.from_defaults(vector_store=store)

    vector_index = VectorStoreIndex.from_vector_store(
        vector_store=store,
        storage_context=storage_context
    )

    vector_retriever = vector_index.as_retriever(similarity_top_k=top_k)

    # mongodb_client.close()
    log.info(f"vector.py read_mongoAtlas: vector retriever returned from mongoAtlas {db_name}/{COLLECTION_NAME}")
    return vector_retriever