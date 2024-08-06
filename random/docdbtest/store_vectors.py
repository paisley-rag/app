# based upon LlamaIndex demo
# https://docs.llamaindex.ai/en/stable/examples/vector_stores/AWSDocDBDemo/


import pymongo
from dotenv import load_dotenv

from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
import os

load_dotenv(override=True)


mongo_uri = os.environ["MONGO_URI"]
mongodb_client = pymongo.MongoClient(mongo_uri)
store = AWSDocDbVectorStore(mongodb_client, db_name='testdb', collection_name='testcollection')
storage_context = StorageContext.from_defaults(vector_store=store)

documents = SimpleDirectoryReader("files").load_data()

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)


response = index.as_query_engine().query('Tell me about Rudenza')
print(f"{response}")


