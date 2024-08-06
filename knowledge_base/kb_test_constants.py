client_sentence_config = {	
    "kb_name": "Sentence",
	"ingest_method": "Simple", 
    "splitter": "Sentence",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "chunk_size": "1024",
        "chunk_overlap": "200"
    },
}

client_semantic_config = {	
    "kb_name": "Semantic",
	"ingest_method": "Simple", 
    "splitter": "Semantic",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "buffer_size": "100",
        "breakpoint_percentile_threshold": "95"
    },
}

client_llama_parse_config = {	
    "kb_name": "Markdown",
	"ingest_method": "LlamaParse", 
    "splitter": "Markdown",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "num_workers": "8"
    },
    "llm_config": {
        "llm_provider": "OpenAI",
        "llm_model": "gpt-3.5-turbo"
    },
}

server_sentence_config = {	
    "kb_name": "Sentence",
	"ingest_method": "Simple", 
    "splitter": "Sentence",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "chunk_size": 1024,
        "chunk_overlap": 200
    },
    "id": "Sentence",
    "files": []
}

server_semantic_config ={	
    "kb_name": "Semantic",
	"ingest_method": "Simple", 
    "splitter": "Semantic",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "buffer_size": 100,
        "breakpoint_percentile_threshold": 95
    },
    "id": "Semantic",
    "files": []
}

server_llama_parse_config = {	
    "kb_name": "Markdown",
	"ingest_method": "LlamaParse", 
    "splitter": "Markdown",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "num_workers": 8
    },
    "llm_config": {
        "llm_provider": "OpenAI",
        "llm_model": "gpt-3.5-turbo"
    },
    "id": "Markdown",
    "files": []
}

