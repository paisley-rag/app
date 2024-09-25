import copy

def chatbot_config(kb_id: str):
    base = {
        "name": "testchatbot",
        "knowledge_bases": [kb_id],
        "generative_model": "gpt-4-o",
        "similarity": {
            "on": False
            },
        "colbert_rerank": {
            "on": False
            },
        "long_context_reorder": {
            "on": False
            },
        "prompt": ""
    }

    similarity_only = copy.deepcopy(base)
    similarity_only['similarity']['on'] = True

    colbert_only = copy.deepcopy(base)
    colbert_only['colbert_rerank']['on'] = True
    colbert_only['colbert_rerank']['top_n'] = 1

    reorder_only = copy.deepcopy(base)
    reorder_only['long_context_reorder']['on'] = True

    similarity_colbert = copy.deepcopy(base)
    similarity_colbert['similarity']['on'] = True
    similarity_colbert['colbert_rerank']['on'] = True
    similarity_colbert['colbert_rerank']['top_n'] = 1

    return {
        'base': base,
        'similarity_only': similarity_only,
        'colbert_only': colbert_only,
        'reorder_only': reorder_only,
        'similarity_colbert': similarity_colbert
    }
