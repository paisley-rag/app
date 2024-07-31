from typing import TypedDict, Optional

# Notes:
# if ingest_method is llama_parse, splitter_config will be a MarkdownConfig and
# llm_config is required
# llm_config is only required for llama_parse

class EmbedConfig(TypedDict):
    embed_provider: str
    embed_model: str

class LLMConfig(TypedDict): 
    llm_provider: str
    llm_model: str


class MarkdownConfig(TypedDict):
    num_workers: int | str # default: 8 

class SemanticConfig(TypedDict):
    buffer_size: int | str # default: 100
    breakpoint_percentile_threshold: int | str # default 95

class SentenceConfig(TypedDict):
    chunk_size: int | str # default 1024
    chunk_overlap: int | str # default: 200


class FileMetadata(TypedDict):
    file_name: str
    content_type: str
    date_uploaded: str
    time_uploaded: str

class ClientKBConfig(TypedDict):
    name: str
    ingest_method: str
    splitter: str
    embed_config: EmbedConfig
    splitter_config: MarkdownConfig | SemanticConfig | SentenceConfig
    llm_config: Optional[LLMConfig] # Only required for llama_parse

class KBConfig(TypedDict):
    name: str
    llm_config: LLMConfig
    embed_config: EmbedConfig
    ingestion_method: str
    splitter: str
    splitter_config: MarkdownConfig | SemanticConfig | SentenceConfig
    llm_config: Optional[LLMConfig] # Only required for llama_parse
    files: list[FileMetadata]