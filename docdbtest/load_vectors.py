# based loosely upon LlamaIndex demo
# https://docs.llamaindex.ai/en/stable/examples/vector_stores/AWSDocDBDemo/
# 
# key goal here was to retrieve the stored vectors from DocumentDB rather than re-create them



import pymongo
from dotenv import load_dotenv

from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
# from llama_index.core import SimpleDirectoryReader
import os

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
mongodb_client = pymongo.MongoClient(mongo_uri)
store = AWSDocDbVectorStore(mongodb_client, db_name='testdb', collection_name='testcollection')
storage_context = StorageContext.from_defaults(vector_store=store)



index = VectorStoreIndex.from_vector_store(
  vector_store=store,
  storage_context=storage_context
)


response = index.as_query_engine().query('Tell me about Rudenza')
print(f"{response}")


