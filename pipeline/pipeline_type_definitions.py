from pydantic import BaseModel
from typing import List

class SimilarityConfig(BaseModel):
    on: str
    similarity_cutoff: str | float

class ColbertRerankConfig(BaseModel):
    on: str
    top_n: str | float

class LongContextReorderConfig(BaseModel):
    on: str

class PostprocessingConfig(BaseModel):
    similarity: SimilarityConfig
    colbert_rerank: ColbertRerankConfig
    long_context_reorder: LongContextReorderConfig

class PromptConfig(BaseModel):
    on: str
    template_str: str

class MyObject(BaseModel):
    name: str
    knowledge_bases: List[str]
    generative_model: str
    postprocessing: PostprocessingConfig
    prompt: PromptConfig

# Example usage:
data = {
    "name": "test3",
    "knowledge_bases": ["66b59d03c78b49c3b890ecac"],
    "generative_model": "gpt-4-o",
    "postprocessing": {
        "similarity": {
            "on": "False",
            "similarity_cutoff": "0.0"
        },
        "colbert_rerank": {
            "on": "False",
            "top_n": "0.0"
        },
        "long_context_reorder": {
            "on": "False"
        }
    },
    "prompt": {
        "on": "False",
        "template_str": "Hello"
    }
}


