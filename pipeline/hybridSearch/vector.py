import os

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
import pymongo

import app_logger as log

load_dotenv(override=True)

# configs
# top_k = 5
environment = os.environ["ENVIRONMENT"]

log.info(f"vector.py: using environment '{environment}'")


# "interface" functions

def write_to_db(db_name, file_path):
    if not os.path.exists(file_path):
        log.debug(f"vector.py: write_to_db - invalid file_path {file_path}")
        return

    if environment == 'local':
        write_local(db_name, file_path)
    elif environment == 'mongoatlas':
        write_mongoAtlas(db_name, file_path)
    else:
        write_prod(db_name, file_path)



def get_retriever(db_name, top_k):
    if environment == 'local':
        return read_local(db_name, top_k)
    elif environment == 'mongoatlas':
        return read_mongoAtlas(db_name, top_k)
    else:
        return read_prod(db_name, top_k)





# local functions (persist to disk)

def write_local(db_name, file_path):
    if os.path.isdir(file_path):
        documents = SimpleDirectoryReader(file_path).load_data()
    else:
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    vector_index = VectorStoreIndex.from_documents(documents)
    vector_index.storage_context.persist(persist_dir=db_name)
    log.info(f"vector.py write_local: {file_path} persist to disk")



def read_local(db_name, top_k):
    vector_storage_context = StorageContext.from_defaults(persist_dir=db_name)

    vector_index = load_index_from_storage(vector_storage_context)

    vector_retriever = vector_index.as_retriever(similarity_top_k=top_k)
    log.info(f"vector.py read_local: vector retriever returned with top_k '{top_k}'")
    return vector_retriever




# "non-local" functions (persist to docdb)

collection_name = 'vector_index'

def mongo():
    mongo_uri = os.environ["MONGO_URI"]
    mongodb_client = pymongo.MongoClient(mongo_uri)
    return mongodb_client


def write_prod(db_name, file_path):
    if os.path.isdir(file_path):
        documents = SimpleDirectoryReader(file_path).load_data()
    else:
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    mongodb_client = mongo()
    store = AWSDocDbVectorStore(
        mongodb_client,
        db_name=db_name,
        collection_name=collection_name
    )
    storage_context = StorageContext.from_defaults(vector_store=store)

    VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    # mongodb_client.close()
    log.info(f"vector.py write_prod: {file_path} written to mongo {db_name}/{collection_name}")


def read_prod(db_name, top_k):
    mongodb_client = mongo()
    store = AWSDocDbVectorStore(
        mongodb_client,
        db_name=db_name,
        collection_name=collection_name
    )
    storage_context = StorageContext.from_defaults(vector_store=store)

    vector_index = VectorStoreIndex.from_vector_store(
        vector_store=store,
        storage_context=storage_context
    )

    vector_retriever = vector_index.as_retriever(similarity_top_k=top_k)

    # mongodb_client.close()
    log.info(f"vector.py read_prod: vector retriever returned from mongo {db_name}/{collection_name}")
    return vector_retriever


# MongoAtlas functions

from llama_index.core.node_parser import SentenceSplitter

def write_mongoAtlas(db_name, file_path):
    if os.path.isdir(file_path):
        documents = SimpleDirectoryReader(file_path).load_data()
    else:
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    nodes = SentenceSplitter(chunk_size=1024, chunk_overlap=20).get_nodes_from_documents(documents)

    mongodb_client = mongo()
    store = MongoDBAtlasVectorSearch(
        mongodb_client,
        db_name=db_name,
        collection_name=collection_name
    )
    storage_context = StorageContext.from_defaults(vector_store=store)

    # VectorStoreIndex.from_documents(
    #     documents, storage_context=storage_context
    # )
    VectorStoreIndex(
        nodes, storage_context=storage_context
    )

    # mongodb_client.close()
    log.info(f"vector.py write_mongoAtlas: {file_path} written to mongoAtlas {db_name}/{collection_name}")


def read_mongoAtlas(db_name, top_k):
    mongodb_client = mongo()
    store = MongoDBAtlasVectorSearch(
        mongodb_client,
        db_name=db_name,
        collection_name=collection_name
    )
    storage_context = StorageContext.from_defaults(vector_store=store)

    vector_index = VectorStoreIndex.from_vector_store(
        vector_store=store,
        storage_context=storage_context
    )

    vector_retriever = vector_index.as_retriever(similarity_top_k=top_k)

    # mongodb_client.close()
    log.info(f"vector.py read_mongoAtlas: vector retriever returned from mongoAtlas {db_name}/{collection_name}")
    return vector_retriever