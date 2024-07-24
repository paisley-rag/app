import os
import pymongo
import nest_asyncio
from dotenv import load_dotenv

from llama_parse import LlamaParse
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext

load_dotenv()
nest_asyncio.apply()

llama_cloud_api_key = os.environ["LLAMA_CLOUD_API_KEY"]
openai_api_key = os.environ["OPENAI_API_KEY"]

mongo_uri = os.environ["MONGO_URI"]
mongodb_client = pymongo.MongoClient(mongo_uri)
docdb_name = os.environ["DOCDB_NAME"]
docdb_collection = os.environ["DOCDB_COLLECTION"]
store = AWSDocDbVectorStore(mongodb_client, db_name=docdb_name, collection_name=docdb_collection)

def send_file_to_llama_parse(file_path):
    print("send_file_to_llama_parse")
    parser = LlamaParse(
        api_key=llama_cloud_api_key,
        result_type="markdown"
    )

    markdown_documents = parser.load_data(file_path)

    print("response received from llama_parse")
    print(markdown_documents[0])
   
    return markdown_documents


# convert markdown documents
# return nodes
def markdown_to_node(documents):
    
    markdown_parser = MarkdownElementNodeParser(
        llm=OpenAI(api_key=openai_api_key, model="gpt-3.5-turbo"),
        num_workers=8,
    )

    nodes = markdown_parser.get_nodes_from_documents(documents)
    print('response from markdown_parser')
    print(nodes[0])

    return nodes

# convert nodes to vector store
# side effect: save index to docdb
def nodes_to_vector_store(nodes):
    embed_model = OpenAIEmbedding(api_key=openai_api_key, model="text-embedding-ada-002")
    storage_context = StorageContext.from_defaults(vector_store=store)
    index = VectorStoreIndex(nodes, embed_model=embed_model, storage_context=storage_context)

    return index

def ingest_file_to_docdb(file_path):

    try:
      markdown_docs = send_file_to_llama_parse(file_path)
      nodes = markdown_to_node(markdown_docs)
      nodes_to_vector_store(nodes)
    except Exception as e:
        raise e
    
