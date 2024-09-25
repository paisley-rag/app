'''
Centralize all .env settings
'''
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    MONGO_URI = os.environ['MONGO_URI']
    CONFIG_DB = os.environ['CONFIG_DB']
    CONFIG_KB_COL = os.environ['CONFIG_KB_COL']
    CONFIG_PIPELINE_COL = os.environ['CONFIG_PIPELINE_COL']
    PAISLEY_ADMIN_USERNAME = os.environ['PAISLEY_ADMIN_USERNAME']
    PAISLEY_ADMIN_PASSWORD = os.environ['PAISLEY_ADMIN_PASSWORD']
    SECRET_KEY = os.environ['JWT_SECRET_KEY']

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    LLAMA_CLOUD_API_KEY = os.getenv('LLAMA_CLOUD_API_KEY', '')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY', '')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

    # temporary directory to store ul'ed files
    FILE_DIR = 'tmpfiles'

    # mongo collectio name used for individual kb vector indexes
    VECTOR_COLLECTION_NAME = 'vector_index'

    # used in chatbot_class
    DEFAULT_TOP_K = 5


    def __getitem__(self, key):
        '''
        allows settings to be accessed as:
            settings.FILE_DIR
        OR  settings['FILE_DIR']
        '''
        return type(self).__dict__[key]

settings = Settings()
