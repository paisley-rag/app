from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
import os

load_dotenv(dotenv_path='../.', override=True)

# configs
persist_dir = 'vectorstorage'
# top_k = 5


def write_to_db(file_path):
    if not file_path:
        print('Need to define file_path')
        return
    documents = SimpleDirectoryReader(file_path).load_data()
    vector_index = VectorStoreIndex.from_documents(documents)
    vector_index.storage_context.persist(persist_dir=persist_dir)
    print('write to disk')


def get_retriever(top_k):
    vector_storage_context = StorageContext.from_defaults(persist_dir=persist_dir)

    vector_index = load_index_from_storage(vector_storage_context)

    vector_retriever = vector_index.as_retriever(similarity_top_k=top_k)
    print('read from disk, return retriever')
    return vector_retriever



