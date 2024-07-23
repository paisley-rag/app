from dotenv import load_dotenv

import pymongo
import os

from llama_parse import LlamaParse
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext

load_dotenv()

mongo_uri = os.environ["MONGO_URI"]
mongodb_client = pymongo.MongoClient(mongo_uri)
store = AWSDocDbVectorStore(mongodb_client, db_name='testdb', collection_name='testcollection')

def send_file_to_llama_parse(file_path):
    parser = LlamaParse(
        api_key=os.environ["LLAMA_PARSE_KEY"],
        result_type="markdown"
    )

    markdown_documents = parser.load_data(file_path)

    return markdown_documents


# convert markdown documents
# return nodes
def markdown_to_node(documents):
    
    markdown_parser = MarkdownElementNodeParser(
        llm=OpenAI(api_key=os.environ["OPENAI_KEY"], model="gpt-3.5-turbo"),
        num_workers=8,
    )

    nodes = markdown_parser.get_nodes_from_documents(documents)
    
    return nodes

# convert nodes to vector store
# side effect: save index to docdb
def nodes_to_vector_store(nodes):
    embed_model = OpenAIEmbedding(api_key=os.environ["OPENAI_KEY"], model="gpt-3.5-turbo")
    storage_context = StorageContext.from_defaults(vector_store=store)

    index = VectorStoreIndex.from_nodes(nodes, embed_model=embed_model)

    index.save_to_storage(storage_context)

    return index

def ingest_file_to_docdb(file_path):
    try:
      markdown_docs = send_file_to_llama_parse(file_path)
      nodes = markdown_to_node(markdown_docs)
      nodes_to_vector_store(nodes)
    except Exception as e:
        print(e)
        raise e
    