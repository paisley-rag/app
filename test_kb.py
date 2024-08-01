import json

import kb_config as kbClass

kb_name = 'giraffe2'

config_template = {
    "id": kb_name,
    "kb_name": kb_name,
    "ingest_method": "Simple",
    "splitter": "Sentence",
    "embed_config": {
        "embed_provider": "OpenAI",
        "embed_model": "text-embedding-3-small"
    },
    "splitter_config": {
        "chunk_size": 1024,
        "chunk_overlap": 200
    }
}

json_config = json.dumps(config_template)
print(json_config)

kbClass.KnowledgeBase.create(json_config)

kb = kbClass.KnowledgeBase('giraffe2')
kb.ingest_file_path('./tmpfiles/giraffes.pdf')



