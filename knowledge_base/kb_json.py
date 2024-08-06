{	
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
    }
}

{	
    "name": "Semantic",
	"ingest_method": "Simple", 
    "splitter": "Semantic",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "buffer_size": "100",
        "breakpoint_percentile_threshold": "95"
    }
}


{	
    "name": "Markdown",
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
    }
}

