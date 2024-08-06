# Testing vector store - no persistence

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()

documents = SimpleDirectoryReader("files").load_data()

index = VectorStoreIndex.from_documents(documents)

print("Index created successfully!")
