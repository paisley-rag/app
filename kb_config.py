'''

Input:
client_kb_config = {
	"name": "kbconfigName",
	"ingest_method": "llama_parse", 
    "splitter": "semantic",
    "embed_model": "openai"
    "chunk_size": "",    # blank for default
	"chunk_overlap": "", # blank for default, number input?  must be smaller than chunk size 
    "separator": "",     # blank for default (" ")


	},
    "files": [],
    "vector_index": "vector_store"
    "keyword_index": "keyword_index"
}

We want this to:
- create a kb_config object and store it in docdb {docdb_name: 'kb_config', docdb_collection: 'kb_config'}
    - docdb should create a unique id for each knowledge base configuration
    - this id will be used to reference the knowledge base configuration in the front end
      ex. when the user selects an already created knowledge base and wants to ingest a new file, that
      file will be associated with the knowledge base configuration id
      ex. when a user creates a knowledge base, the client_kb_config object will be passed into the
      KB_CREATE class to create a new knowledge base

- When the user uploads a file to a particular knowledge base, the kb_config object will be passed into 
	KB_Instaintiate class to define file ingestion pipeline


CreateKB
- api/create_kb takes a client_kb_config object
- validate cliet_kb_config['name'] is unique
- creates a kb_config object
- stores the kb_config object in docdb
- responds to client with the kb_config_id

AddDataToKB class:
for skateboard
- api/upload_file (name for temporary clarity assuming other data sources in the future and the possibility they are routed elsewhere)
- recieves a file and a kb_config_id from the client
	{
		"file": file,
		"kb_config_id": kb_config_id
	}
- uses the kb_config_id to retrieve the kb_config object from docdb
- instantiates AddDataToKB class with the kb_config object
- calls the ingest_file method on the AddDataToKB object, passing in the file path



AddDataToKB class:
-ingestion methods:
	- ingest_file method
	future tripping:
		- ingest_url method
		- ingest_repo method

- ingest_file method:
	- takes a file path
	- chunks and embeds according to the AddDataToKB configuration
	- stores indexes in docdb
		- VectorStoreIndex
		- KeywordIndex
		- etc. 


'''

'''
Implementation Plan:
    - create_knowledge_base accepts a simplified client_kb_config object 
    (ingest_method, spliter, embed_model) and stores it in docdb
- create simple instance of class with id 
    - use id to retrieve kb_config object from docdb
    - use config object to define ingestion pipeline
- ingest file with pipeline defined by kb_config object
    - load file according to ingest_method
    - split file according to splitter
    - embed file according to embed_model
    - store indexes in docdb

- consider replacing with built in ingestion pipeline

- obscure the id values used to fetch the knowledge base from
    the client side for now, this is implemented to use the 
    name of the mongo(docdb) db to store the knowledge base

- add bedrock functionality

- be sure to convert strings to integers when necessary

- pull file from s3 bucket rather than local file system

- add flexibility for llms in MarkdownElementNodeParser
    - currently only OpenAI is supported

- do we want to store nodes or documents in keyword index?
    - currently storing nodes

- write `_config` methods for embed model

- refactor 
    - make duplicate values/ opperations properties of the class

- integrate with front end


'''
from typing import TypedDict, Optional

import copy
import os
import app_logger as log
from dotenv import load_dotenv
import pymongo
import nest_asyncio


# imports for reading files
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# imports for parsing files
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
    MarkdownElementNodeParser
)

# index storage imports
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
# from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore

# imports for embedding models
from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.embeddings import BedrockEmbedding

# imports for llms
from llama_index.llms.openai import OpenAI

class ClientKBConfig(TypedDict):
    name: str
    ingest_method: str
    splitter: str
    embed_model: str
    embed_model_name: str
    chunk_size: Optional[str]
    chunk_overlap: Optional[str]
    separator: Optional[str]

class IndexDict(TypedDict):
    name: str
    collection: str

class KBConfig(TypedDict):
    name: str
    ingest_method: str
    splitter: str
    embed_model_class: str
    embed_model_name: str
    chunk_size: Optional[str]
    chunk_overlap: Optional[str]
    separator: Optional[str]
    files: list
    vector_index: IndexDict
    keyword_index: IndexDict

val = 2


class KnowledgeBase:
    def __init__(self, name):
        self.options = {
            "ingest_method": {
                "simple_ingest": SimpleDirectoryReader,
                "llama_parse": LlamaParse
            },
            "splitter": {
                "sentence": SentenceSplitter,
                "semantic": SemanticSplitterNodeParser
            },
            "embed_model_class": {
                "openai": OpenAIEmbedding,
                # "bedrock": BedrockEmbedding
            },

        }
        self.config = self._get_kb_config(name)

        self.ingest = self.options["ingest_method"][self.config['ingest_method']]
        self.splitter = self.options["splitter"][self.config['splitter']]
        self.embed_model_class = self.options["embed_model_class"][self.config['embed_model_class']]
        
        # 200 is the baked in default from SentenceSplitter source code
        # I considered that passing in None as the default might 
        # create errors as the simplest way to configure these optional
        # params is to always pass an argument. 
        # ex. SentenceSplitter(chunk_overlap=self.chunk_overlap)
        # This should get us out of potential conditional statement 
        # hell. 
        self.chunk_overlap = int(self.config.get('chunk_overlap')) if self.config.get('chunk_overlap') else 200

        # IMO, these should be available as options for TokenTextSplitter
        # but not sentence splitter
        # self.chunk_size = self.config['chunk_size'] | None
        # self.separator = self.config['separator'] | None
    
    @classmethod
    def create_knowledge_base(cls, client_config: ClientKBConfig):
        kb_config = cls._create_kb_config(client_config)
        pymongo_client = pymongo.MongoClient(os.environ["MONGO_URI"])
        # ostensibly, we could use one db for many collections
        # and designate the collection as the knowledge base
        db_name = os.environ["KB_CONFIG_DOCDB"]
        # also, I know this is a really long name, but it's
        # descriptive and clear
        collection_name = os.environ["KB_CONFIG_COLLECTION_DOCDB"]
        # Connect to the MongoDB client
    

        # Select the database
        db = pymongo_client[db_name]

        # Select the collection
        collection = db[collection_name]

        # Insert the object into the collection
        result = collection.insert_one(kb_config)
        print(result.inserted_id)
        



    @classmethod
    def _create_kb_config(cls, client_config: ClientKBConfig) -> KBConfig:
        kb_config = copy.copy(client_config)
        kb_config["chunk_overlap"] = int(client_config["chunk_overlap"])
        kb_config['files'] = []

        kb_config['vector_index'] = {
            'name': kb_config['name'],
            'collection': kb_config['name']
        }

        kb_config['keyword_index'] = {
            'name': kb_config['name'],
            'collection': kb_config['name']
        }
        return kb_config
    
    def _get_kb_config(self, name):
        pymongo_client = pymongo.MongoClient(os.environ["MONGO_URI"])
        db_name = os.environ["KB_CONFIG_DOCDB"]
        collection_name = os.environ["KB_CONFIG_COLLECTION_DOCDB"]
        db = pymongo_client[db_name]
        collection = db[collection_name]
        return collection.find_one({"name": name})
    

    def _config_llama_parse(self):
        parser = LlamaParse(
            api_key=os.environ["LLAMA_CLOUD_API_KEY"],
            result_type="markdown"
        )
        return parser
    
    def _config_markdown_chunker(self):
        markdown_parser = MarkdownElementNodeParser(
            llm=OpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo"),
            num_workers=8,
        )
        return markdown_parser
    
    def _config_semantic_splitter(self):
        embed_model = OpenAIEmbedding(
            api_key=os.environ["OPENAI_API_KEY"],
            model="text-embedding-ada-002"
        )

        splitter = SemanticSplitterNodeParser(
            buffer_size=100,
            breakpoint_percentile_threshold=95,
            embed_model=embed_model,
        )

        return splitter
    
    def _config_sentece_splitter(self):
        splitter = SentenceSplitter(
            chunk_overlap=self.chunk_overlap
        )

        return splitter
           
    # saves file locally, returns file path
    def _save_file_locally(self, file):
        FILE_DIR = 'tmpfiles'

        # write file to disk
        if not os.path.exists(f"./{FILE_DIR}"):
            os.makedirs(f"./{FILE_DIR}")

        file_path = f"./{FILE_DIR}/{file.filename}"

        return file_path
    
    def _create_nodes(self, file_path):
        if self.config['ingest_method'] == 'llama_parse':
            llama_parse = self._config_llama_parse()
            markdown_documents = llama_parse.load_data(file_path)
            markdown_chunker = self._config_markdown_chunker()
            nodes = markdown_chunker.get_nodes_from_documents(markdown_documents)
            return nodes
        
        documents = self.ingest(input_files=[file_path]).load_data()
        
        if self.config['splitter'] == 'semantic':
            splitter = self._config_semantic_splitter()
            nodes = splitter.get_nodes_from_documents(documents)
        
        elif self.config['splitter'] == 'sentence':
            splitter = self._config_sentece_splitter()
            nodes = splitter.split(documents)

        return nodes
    
    def _store_indexes(self, nodes):
        mongo_uri = os.environ["MONGO_URI"]
        mongodb_client = pymongo.MongoClient(mongo_uri)
        docdb_name = os.environ["DOCDB_NAME"]
        docdb_collection = os.environ["DOCDB_COLLECTION"]
        store = MongoDBAtlasVectorSearch(mongodb_client, db_name=docdb_name, collection_name=docdb_collection)
        storage_context = StorageContext.from_defaults(vector_store=store)
        embed_model = OpenAIEmbedding(
            api_key=os.environ["OPENAI_API_KEY"],
            model="text-embedding-ada-002"
        )
        index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embed_model)


    def ingest_file(self, file):
        file_path = self._save_file_locally(file)
        nodes = self._create_nodes(file_path)
        self._store_indexes(nodes)
        
        
    

        # how do we handle the ingest options?
        # 

        


    def print_config(self):
        print(self.chunk_overlap)
    


kb = KnowledgeBase('kbconfigName2')

kb.ingest_file('file')


# client_kb_config = {
# 	"name": "kbconfigName2",
# 	"ingest_method": "simple_ingest", 
#     "splitter": "semantic",
#     "embed_model_class": "openai",
#     "embed_model_name": "text-embedding-ada-002",
#     "chunk_size": "",    # blank for default
# 	  "chunk_overlap": "", # blank for default, number input?  must be smaller than chunk size 
#     "separator": "",     # blank for default (" ")
#     "llm":
# }


# KnowledgeBase.create_knowledge_base(client_kb_config)

# # initializing local variable to class test
# value = OpenAIEmbedding
# print(value)
# print(value.__name__)
# embed_model = value(api_key='key', model='text-embedding-ada-002')

# class Test:
#     def __init__(self, data):
#       self.updated_data = self.update_data(data)
    
#     def update_data(self, data):
#       return data + 1
    
#     def get_data(self):
#       return self.updated_data
    
#     def set_d2(self):
#       self.d2 = 4

#     def get_d2(self):
#       return self.d2
	

	
# value = Test(1)
# value.set_d2()
# print(value.get_d2())