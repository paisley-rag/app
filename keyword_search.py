from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
# from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore
from llama_index.core import StorageContext
from dotenv import load_dotenv
import pymongo
import Stemmer
import os

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
store = MongoDocumentStore.from_uri(mongo_uri, 'keyword')

storage_context = StorageContext.from_defaults(
    docstore=MongoDocumentStore.from_uri(uri=mongo_uri, db_name='keyword'),
    index_store=MongoIndexStore.from_uri(uri=mongo_uri, db_name='keyword')
)



documents = SimpleDirectoryReader('./tmpfiles').load_data()
splitter = SentenceSplitter(chunk_size=512)

nodes = splitter.get_nodes_from_documents(documents)

storage_context.docstore.add_documents(nodes)


bm25_retriever = BM25Retriever.from_defaults(
    docstore=store,
    similarity_top_k=5,
    stemmer=Stemmer.Stemmer('english'),
    language='english',
)

retrieved_nodes = bm25_retriever.retrieve("associative")

for node in retrieved_nodes:
    print(node)


mongodb = pymongo.MongoClient(mongo_uri)
db = mongodb['keyword']
print(db.list_collection_names())


