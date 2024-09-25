'''
defines knowledge_base class
'''
import os
import shutil
from datetime import datetime, timezone

import nest_asyncio
from llama_index.core import VectorStoreIndex

from db.util import use_s3
import db.app_logger as log
from db.config import settings

from db.knowledge_base.kb_constants import (
    EMBEDDINGS,
    INGEST_METHODS,
    SPLITTERS,
    LLMS,
    API_KEYS,
)

nest_asyncio.apply()

class KnowledgeBase:
    # props in `self._config` are str names of the knowledge base configuration
    # self._embed_model, self._llm, and self._splitter are instances of the classes
    # defined by properties in `self._config`
    # self._ingest_method is the class of the ingestion method defined by the
    # ingest_method property in `self._config`

    def __init__(self, kb_name, db):
        self._db = db
        self._id = kb_name
        self._config = self._get_kb_config(kb_name)
        self._embed_model = self._configure_embed_model()
        self._llm = self._configure_llm()
        self._ingest_method = INGEST_METHODS[
            self._config['ingest_method']
        ]
        self._splitter = self._configure_splitter()

    # returns the configuration object for a knowledge base
    def _get_kb_config(self, get_id):
        kb_config = self._db.get_knowledge_base(get_id)
        log.info('kb_config.py _get_kb_config: ', kb_config)
        return kb_config

    def _configure_embed_model(self):
        embed_provider = self._config['embed_config']['embed_provider']
        embed_model_class = EMBEDDINGS[embed_provider]
        api_key = settings[API_KEYS[embed_provider]]
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
        log.info('kb_config.py _save_file_locally: ', file.filename, self._id)

        # write file to disk
        if not os.path.exists(f"./{settings.FILE_DIR}"):
            os.makedirs(f"./{settings.FILE_DIR}")

        file_path= f"./{settings.FILE_DIR}/{file.filename}"

        with open(file_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        use_s3.ul_file(file, self._id)

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

        log.info('kb_config.py _store_indexes: ********* ', self._config)

        kb_id = self._db.get_kb_id(self._config['kb_name'])
        log.info('kb_config.py _store_indexes: ', kb_id)

        # vector index
        storage_context = self._db.get_vector_storage_context(kb_id)

        VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=self._embed_model
        )

        # keyword index
        self._db.get_keyword_store(kb_id).add_documents(nodes)

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

        log.info('kb_class._add_file_to_kb_config: ', file, file_metadata)

        self._db.add_file_metadata_to_kb(
            self._config['kb_name'],
            file_metadata
        )

        self._config = self._get_kb_config(self._id)

    async def ingest_file(self, file):
        file_path = self._save_file_locally(file)
        nodes = await self._create_nodes(file_path)
        self._store_indexes(nodes)
        self._add_file_to_kb_config(file)
