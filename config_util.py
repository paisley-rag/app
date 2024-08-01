import json

import app_logger as log

DEFAULT_TOP_N = 5

def ui_to_pipeline(ui_json):
    # note:  takes in json, returns an obj

    ui_obj = json.loads(ui_json)
    log.info('config_util.py ui_to_pipeline: ui_obj', ui_obj)

    pipeline_obj = {
        'id': str(ui_obj['id']),
        'name': ui_obj['name'],
        'knowledgebases': ui_obj['knowledge_bases'],
        'postprocessing': {
            'similarity': {
                'on': ui_obj['similarity']['on'],
                'similarity_cutoff': ui_obj['similarity'].get('cutoff', 0.7),
            },
            'colbertRerank': {
                'on': ui_obj['colbert_rerank']['on'],
                'top_n': ui_obj['colbert_rerank'].get('top_n', DEFAULT_TOP_N)
            },
            'longContextReorder': {
                'on': ui_obj['long_context_reorder'],
            }
        },
        'generative_model': ui_obj['generative_model'],
        'prompt': {
            'on': True if ui_obj.get('prompt') else False,
            'template_str': ui_obj.get('prompt', '')
        }
    }

    log.info('config_util.py ui_to_pipeline: pipeline_obj', pipeline_obj)
    return pipeline_obj


