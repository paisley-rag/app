import os

from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.cohere import Cohere

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.cohere import CohereEmbedding
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# imports for reading files
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# imports for parsing files
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
    MarkdownElementNodeParser
)

LLMS = {
    "OpenAI": OpenAI,
    "Anthropic": Anthropic,
    "Cohere": Cohere
}

EMBEDDINGS = {
    "OpenAI": OpenAIEmbedding,
    "Cohere": CohereEmbedding,
}

INGESTION_METHODS = { 
    "LlamaParse": LlamaParse,
    "Simple": SimpleDirectoryReader
}

SPLITTERS = {
    "Sentence": SentenceSplitter,
    "Semantic": SemanticSplitterNodeParser,
    "Markdown": MarkdownElementNodeParser
}

API_KEYS = {
    "OpenAI": "OPENAI_API_KEY",
    "Cohere": "COHERE_API_KEY",
    "Anthropic": "ANTHROPIC_API_KEY",
    "LlamaParse": "LLAMA_CLOUD_API_KEY",
}




LLM_MODELS = {
    "OpenAI": [
        {
            "name": "gpt-3.5-turbo",
            "description": "good balance of cost and precision",
        },  
        {
            "name": "gpt-4-turbo",
            "description": "more advanced than 'gpt-3.5-turbo'",
        },  
        {
            "name": "gpt-4o-mini",
            "description": "affordable small model for lightweight tasks",
        },
        {
            "name": "gpt-4o",
            "description": "OpenAI's flagship model",
        }
    ],

    "Anthropic": [
        {
            "name": "claude-4-haiku-20240307",
            "description": "fastest and cheapest Anthropic model",
        },
        {
            "name": "claude-3-sonnet-20240229",
            "description": "balanced intellegence and speed",
        },
        {
            "name": "claude-3-5-sonnet-20240620",
            "description": "highest performing Anthropic model",
        }
    ],
    "Cohere": []
}


EMBEDDING_MODEL_DETAILS = {
    "OpenAI": [
        {
            "name": "text-embedding-3-small",
            "description": "good balance of cost and precision", 
            "language": "multilingual",
        },
        {
            "name": "text-embedding-3-large",
            "description": "slightly more precise at ~6 times the cost of 'text-embedding-3-small'",
            "language": "multilingual"
        }
    ],
    "Cohere": [
        {
            "name": "embed-english-light-v3.0", 
            "description": "slightly less precise, but faster than 'embed-english-v3.0'",
            "language": "english"
        },
        {
            "name": "embed-english-v3.0",
            "description": "more precise, but slower than 'embed-english-light-v3.0'",
            "language": "english"    
        },
        {
            "name": "embed-multilingual-light-v3.0",
            "description": "slightly less precise, but faster than 'embed-multilingual-v3.0'",
            "language": "multilingual"
        }, 
        {
            "name": "embed-multilingual-v3.0",
            "description": "more precise, but slower than 'embed-multilingual-light-v3.0'",
            "language": "multilingual"
        },       
    ],
}





'''
Need to test hugging face embedding



'''