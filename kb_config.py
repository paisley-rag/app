import copy
import os
import use_s3
import shutil
import app_logger as log
from dotenv import load_dotenv
# import pymongo
import mongo_helper as mongo
import nest_asyncio
import use_s3
import shutil
from datetime import datetime, timezone

# storage imports
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
# from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.storage.docstore.mongodb import MongoDocumentStore

from kb_constants import (
    EMBEDDINGS,
    INGEST_METHODS,
    SPLITTERS,
    LLMS,
    API_KEYS,
)

from kb_type_definitions import (
    EmbedConfig,
    LLMConfig,
    MarkdownConfig,
    SemanticConfig,
    SentenceConfig,
    FileMetadata,
    ClientKBConfig,
    KBConfig
)

# MONGO_URI = os.environ["MONGO_URI"]
# CONFIG_DB = os.environ["CONFIG_DB"]
# CONFIG_KB_COL = os.environ["CONFIG_KB_COL"]
# PYMONGO_CLIENT = pymongo.MongoClient(MONGO_URI)
# CONFIG_COLLECTION = PYMONGO_CLIENT[CONFIG_DB][CONFIG_KB_COL]

CONFIG_COLLECTION = mongo.connect_to_kb_config()

load_dotenv()

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class KnowledgeBase:

    # props in `self._config` are str names of the knowledge base configuration 
    # self._embed_model, self._llm, and self._splitter are instances of the classes
    # defined by properties in `self._config`
    # self._ingest_method is the class of the ingestion method defined by the
    # ingest_method property in `self._config`
    def __init__(self, kb_name):
        self._config = self._get_kb_config(kb_name)
        self._embed_model = self._configure_embed_model()
        self._llm = self._configure_llm()
        self._ingest_method = INGEST_METHODS[
            self._config['ingest_method']
        ]
        self._splitter = self._configure_splitter()
    
    @classmethod
    def create(cls, client_config):
        # add properties to client_config
        kb_config = cls._create_kb_config(client_config)           
        log.info(kb_config)
        # insert knowledge base configuration into database
        result = CONFIG_COLLECTION.insert_one(kb_config)
        log.info(result)

        # message for client
        return "Knowledge base created"

    @classmethod
    def _create_kb_config(cls, client_config):
        kb_config = copy.copy(client_config)

        kb_config['splitter_config'] = cls._str_to_nums(kb_config['splitter_config'])
        kb_config['files'] = []

        return kb_config
    
    # converts ints and floats in a dictionary to their respective types
    @classmethod
    def _str_to_nums(cls, config_dict):
        result = {}
        for key in config_dict:
            if is_int(config_dict[key]):
                result[key] = int(config_dict[key])
            elif is_float(config_dict[key]):
                result[key] = float(config_dict[key])
            else:
                result[key] = config_dict[key]
        
        return result
    
    # returns None if not found, otherwise returns the document
    @classmethod
    def exists(cls, kb_name):
        return CONFIG_COLLECTION.find_one({"kb_name": kb_name})

    # returns list of file metadata objects for a knowledge base
    def get_files(self, kb_name):
        return CONFIG_COLLECTION.find_one({"kb_name": kb_name})['files']

    # returns the configuration object for a knowledge base
    def _get_kb_config(self, kb_name):
        return CONFIG_COLLECTION.find_one({"kb_name": kb_name})
    
    def _configure_embed_model(self):
        embed_provider = self._config['embed_config']['embed_provider']
        embed_model_class = EMBEDDINGS[embed_provider]
        api_key = os.environ[API_KEYS[embed_provider]]
        model = self._config['embed_config']['embed_model']
        embed_model = embed_model_class(api_key=api_key, model=model)
        
        return embed_model

    
    def _configure_llm(self):
        if self._config.get('llm_config') is None:
            return None
        
        llm_provider = LLMS[self._config['llm_config']['llm_provider']]
        key_name = API_KEYS[self._config['llm_config']['llm_provider']]
        llm = llm_provider(
            api_key=os.environ[key_name],
            model= self._config['llm_config']['llm_model']
        )

        return llm

    def _configure_splitter(self):
        splitter_config = self._config['splitter_config']
        splitter_name = self._config['splitter']

        if splitter_name == 'Semantic':
            splitter_config['embed_model'] = self._embed_model
        elif splitter_name == 'Markdown':
            splitter_config['llm'] = self._llm
        
        splitter_class = SPLITTERS[self._config['splitter']]

        return splitter_class(**self._config['splitter_config'])        
    
    
    # handles llama parse ingestion, returns semantic markdown nodes
    # def _run_llama_parse(self, file_path):
    #     llama_parse = self._config_llama_parse()
    #     markdown_documents = llama_parse.load_data(file_path)
    #     markdown_chunker = self._config_markdown_chunker()
    #     nodes = markdown_chunker.get_nodes_from_documents(markdown_documents)
    #     return nodes
    
    # def _config_llama_parse(self):
    #     parser = LlamaParse(
    #         api_key=os.environ["LLAMA_CLOUD_API_KEY"],
    #         result_type="markdown"
    #     )
    #     return parser
    
    # def _config_markdown_chunker(self):
    #     # make llm configurable
    #     markdown_parser = MarkdownElementNodeParser(
    #         llm=OpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo"),
    #         num_workers=8,
    #     )

    #     return markdown_parser
    
    # def _config_semantic_splitter(self):
    #     # make embed model configurable
    #     embed_model = OpenAIEmbedding(
    #         api_key=os.environ["OPENAI_API_KEY"],
    #         model="text-embedding-ada-002"
    #     )
    #     # make configurable
    #     splitter = SemanticSplitterNodeParser(
    #         buffer_size=100,
    #         breakpoint_percentile_threshold=95,
    #         embed_model=embed_model,
    #     )

    #     return splitter
    
    # def _config_sentence_splitter(self):
    #     splitter = SentenceSplitter(
    #         chunk_overlap=self.chunk_overlap
    #     )

    #     return splitter
           
    # saves file locally, returns file path
    def _save_file_locally(self, file):
        FILE_DIR = 'tmpfiles'

        # write file to disk
        if not os.path.exists(f"./{FILE_DIR}"):
            os.makedirs(f"./{FILE_DIR}")


        file_path= f"./{FILE_DIR}/{file.filename}"

        with open(file_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        # use_s3.ul_file(file.filename, dir=FILE_DIR)

        return file_path
    
    def _create_nodes(self, file_path):
        if self._config['ingest_method'] == 'LlamaParse':
            llama_parse = self._ingest_method(
                api_key=os.environ["LLAMA_CLOUD_API_KEY"],
                result_type="markdown"
            )
            documents = llama_parse.load_data(file_path)
        else:
            documents = self._ingest_method(input_files=[file_path]).load_data()
            
        
        if self._config['splitter'] == 'sentence':
            nodes = self._splitter.split(documents)
        else:
            nodes = self._splitter.get_nodes_from_documents(documents)

        return nodes
    
    def _store_indexes(self, nodes):
        
        mongodb_client = mongo.client()
        # database name defines a knowledge base
        kb_id = str(self._config['_id'])
        vector_index = "vector_index"

        vector_store = MongoDBAtlasVectorSearch(
            mongodb_client,
            db_name=kb_id,
            collection_name=vector_index
        )

        # vector_store = AWSDocDbAtlasVectorSearch(
        #     mongodb_client,
        #     db_name=kb_id,
        #     collection_name=vector_index
        # )

        docstore = MongoDocumentStore.from_uri(
            uri=os.environ["MONGO_URI"],
            db_name=kb_id
        )

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            # docstore=docstore    
        )

        docstore.add_documents(nodes)
        VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=self._embed_model
        )
        
    def _add_file_to_kb_config(self, file):
        now = datetime.now(timezone.utc)
        date = now.strftime("%m-%d-%y")
        time = now.strftime("%H:%M")

        CONFIG_COLLECTION.update_one(
            {"kb_name": self._config['kb_name']},
            {"$push": {
                "files": {
                    "file_name": file.filename,
                    "content_type":file.headers['content-type'],
                    "date_uploaded": date,
                    "time_uploaded": time
                    }
                }
            }
        )


    def ingest_file(self, file):
        file_path = self._save_file_locally(file)
        nodes = self._create_nodes(file_path)
        self._store_indexes(nodes)
        self._add_file_to_kb_config(file)


        


    def print_config(self):
        print(self.chunk_overlap)
    


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
}

kb_config = {
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

- test adding file to vector index

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

- update 'name' in vector index and keyword index to be database name

- update line 264 to manage empty strings

- add s3 bucket functionality

- write down database names

- when a file is uploaded, store the file metadata in the assiciated knowledge base
    configuration file in knowledge base configuration database


- each knowledge base's vector index and keyword index are stored in the same database
    Database defines knowledge base



'''
