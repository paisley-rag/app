import os
import shutil
from datetime import datetime, timezone

import pymongo
import use_s3
import nest_asyncio
from dotenv import load_dotenv
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.vector_stores.awsdocdb import AWSDocDbVectorStore
from llama_index.storage.docstore.mongodb import MongoDocumentStore


import db.app_logger as log
from db.knowledge_base import mongo_helper as mongo

from db.knowledge_base.kb_constants import (
    EMBEDDINGS,
    INGEST_METHODS,
    SPLITTERS,
    LLMS,
    API_KEYS,
)

from db.knowledge_base.kb_type_definitions import (
    EmbedConfig,
    LLMConfig,
    MarkdownConfig,
    SemanticConfig,
    SentenceConfig,
    FileMetadata,
    ClientKBConfig,
    KBConfig
)


env = os.getenv("ENV")
print("env: ", env)
if env == 'testing':
    load_dotenv(override=True, dotenv_path='../.env.testing')
else:
    load_dotenv(override=True)

MONGO_URI = os.environ["MONGO_URI"]

nest_asyncio.apply()

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
    
    # returns the configuration object for a knowledge base
    def _get_kb_config(self, id):
        kb_config = mongo.get_knowledge_base(id)
        log.info('kb_config.py _get_kb_config: ', kb_config)
        return kb_config
    
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
    
    
           
    # saves file locally, returns file path
    def _save_file_locally(self, file):
        FILE_DIR = 'tmpfiles'
        log.info('kb_config.py _save_file_locally: ', file.filename)
        # write file to disk
        if not os.path.exists(f"./{FILE_DIR}"):
            os.makedirs(f"./{FILE_DIR}")


        file_path= f"./{FILE_DIR}/{file.filename}"

        with open(file_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        use_s3.ul_file(file.filename, dir=FILE_DIR)

        return file_path
    
    async def _create_nodes(self, file_path):
        if self._config['ingest_method'] == 'LlamaParse':
            llama_parse = self._ingest_method(
                api_key=os.environ["LLAMA_CLOUD_API_KEY"],
                result_type="markdown"
            )
            try: 
                documents = llama_parse.load_data(file_path)
                log.info('kb_config.py _create_nodes: ', documents)
            except Exception as e:
                log.error('kb_config.py _create_nodes: ', e)
                return e
        else:
            documents = self._ingest_method(input_files=[file_path]).load_data()
            
        
        if self._config['splitter'] == 'sentence':
            log.info('sentence splitter used')
            nodes = self._splitter.split(documents)
        else:
            nodes = self._splitter.get_nodes_from_documents(documents)

        return nodes
    
    def _store_indexes(self, nodes):
        
        client = pymongo.MongoClient(MONGO_URI)
        
        log.info('kb_config.py _store_indexes: ********* ', self._config)

        kb_id = mongo.get_kb_id(self._config['kb_name'])
        log.info('kb_config.py _store_indexes: ', kb_id)
        vector_index = "vector_index"

        environment = os.getenv('ENVIRONMENT', 'production')

        if environment == 'local' or environment == 'mongoatlas':
            vector_store = MongoDBAtlasVectorSearch(
                client,
                db_name=kb_id,
                collection_name=vector_index
            )
        else:
            vector_store = AWSDocDbVectorStore(
                client,
                db_name=kb_id,
                collection_name=vector_index
            )


        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            # docstore=docstore    
        )

        VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=self._embed_model
        )

        docstore = MongoDocumentStore.from_uri(
            uri=MONGO_URI,
            db_name=kb_id
        )

        docstore.add_documents(nodes)
        client.close()
 
    def _add_file_to_kb_config(self, file):
        now = datetime.now(timezone.utc)
        date = now.strftime("%m-%d-%y")
        time = now.strftime("%H:%M")
        size = file.size


        file_metadata = {
            "file_name": file.filename,
            "content_type": file.headers["content-type"],
            "date_uploaded": date,
            "time_uploaded": time,
            "size": size
        }

        mongo.add_file_metadata_to_kb(
            self._config['kb_name'],
            file_metadata
        )


    async def ingest_file(self, file):
        file_path = self._save_file_locally(file)
        nodes = await self._create_nodes(file_path)
        self._store_indexes(nodes)
        self._add_file_to_kb_config(file)

    # def ingest_file_path(self, file_path):
    #     nodes = self._create_nodes(file_path)
    #     self._store_indexes(nodes)
    #     self._add_file_to_kb_config(file_path)

    # def print_config(self):
    #     print(self.chunk_overlap)
    

    # # @classmethod
    # # def create(cls, client_config):
    # #     # add properties to client_config
    # #     kb_config = cls._create_kb_config(client_config)
    # #     log.info("kb_config.py create (classmethod): ", kb_config)
    # #     # insert knowledge base configuration into database
    # #     result = mongo.insert_knowledge_base(kb_config)
    # #     log.info("kb_config.py create (classmethod): ", result)
    # #     name = kb_config["kb_name"]
    # #     # message for client
    # #     return f"{name} created"

    # # @classmethod
    # # def _create_kb_config(cls, client_config):
    # #     kb_config = copy.copy(client_config)
    # #     log.info('kb_config.py _create_kb_config: ', client_config, kb_config)
    # #     kb_config['id'] = kb_config['kb_name']
    # #     kb_config['splitter_config'] = cls._str_to_nums(kb_config['splitter_config'])
    # #     kb_config['files'] = []

    # #     return kb_config
    
    # # # converts ints and floats in a dictionary to their respective types
    # # @classmethod
    # # def _str_to_nums(cls, config_dict):
    # #     result = {}
    # #     for key in config_dict:
    # #         if is_int(config_dict[key]):
    # #             result[key] = int(config_dict[key])
    # #         elif is_float(config_dict[key]):
    # #             result[key] = float(config_dict[key])
    # #         else:
    # #             result[key] = config_dict[key]
        
    # #     return result
    
    # # returns None if not found, otherwise returns the document
    # @classmethod
    # def exists(cls, kb_name):
    #     print(kb_name)
    #     doc = mongo.get_knowledge_base(kb_name)
    #     print(doc)
    #     log.info('kb_config.py exists: ', doc)
    #     return doc

    # @classmethod
    # def get_knowledge_bases(cls):
    #     kbs_cursor = mongo.get_knowledge_bases()
    #     kbs_list = list(kbs_cursor)
    #     print('kb_config.py get_knowledge_bases: ', kbs_list)
    #     # log.info('kb_config.py get_knowledge_bases: ', kbs)
    #     return kbs_list