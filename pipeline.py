import asyncio

from llama_index.core import QueryBundle
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LongContextReorder
from llama_index.postprocessor.colbert_rerank import ColbertRerank
from llama_index.core import get_response_synthesizer, PromptTemplate
from llama_index.core.response_synthesizers import ResponseMode

import app_logger as log
import hybridSearch.search as search

class Pipeline:
    def __init__(self, config_json):
        self._config = self._parse_json(config_json)

    def query(self, user_query):
        synthesizer, nodes = self._pipeline(user_query).values()
        return synthesizer.synthesize(user_query, nodes=nodes)


    def _pipeline(self, user_query):
        # get a retriever from each knowledge base
        retrievers = self._process_kbs(['1']) # generic kb for testing

        # query each knowledge base and get returned_nodes
        # all_nodes = asyncio.run(self._query_retriever(retrievers, user_query))
        all_nodes = self._query_retriever(retrievers, user_query)

        log.info(f"pipeline.py _pipeline: all_nodes")
        self._log_nodes(all_nodes)

        # post-processing
        nodes_similar = self._process_similarity(all_nodes)

        log.info('nodes_similar')
        self._log_nodes(nodes_similar)

        nodes_rerank = self._process_colbert(nodes_similar, user_query)


        log.info('nodes_rerank')
        self._log_nodes(nodes_rerank)

        nodes_reorder = self._process_reorder(nodes_rerank)

        log.info('nodes_reorder')
        self._log_nodes(nodes_reorder)

        synth = get_response_synthesizer(
            response_mode=ResponseMode.SIMPLE_SUMMARIZE
        )

        # need to add custom prompts
        return { 'synthesizer': synth, 'nodes': nodes_reorder }


    # Knowledge base methods
    def _process_kbs(self, kb_ids):
        retrievers = list(map(self._get_retriever, kb_ids))
        log.info(f"pipeline.py _process_kbs: returned {len(retrievers)} retrievers", retrievers)
        return retrievers


    def _get_retriever(self, kb_id):
        log.info(f"pipeline.py _get_retriever: {kb_id} received")

        # just return existing knowledge bases for testing
        vector_retriever = search.vector_retriever()
        keyword_retriever = search.keyword_retriever()
        return { 'vector': vector_retriever, 'keyword': keyword_retriever }


    # Retrieval methods
    def _query_retriever(self, retrievers, user_query):
        nodes = []
        for obj in retrievers:
            nodes += obj['vector'].retrieve(user_query)
            nodes += obj['keyword'].retrieve(user_query)

        return nodes

    # async def _use_retriever(self, retriever, user_query):
    #     return retriever.retrieve(user_query)

    # async def _query_retriever(self, retrievers, user_query):
    #     log.info(f"pipeline.py _query_retriever: ", retrievers)
    #     nodes = []

    #     for obj in retrievers:
    #         rets = [ obj['vector'], obj['keyword']]
    #         ops = [self._use_retriever(retriever, user_query) for retriever in rets]

    #         result = await asyncio.gather(*ops)


    #     log.info(f"pipeline.py _query_retriever: all nodes", self._log_nodes(result))
    #     return nodes



    # Post-processing methods
    def _process_similarity(self, nodes):
        options = self._get_options('similarity')

        if not options['on']:
            return nodes

        log.debug(f"pipeline.py _process_similarity: ", self._remove_on(options))

        similarity_pp = SimilarityPostprocessor(**self._remove_on(options))
        log.info(f"pipeline.py _process_similarity: cutoff of {options['similarity_cutoff']} applied")
        return similarity_pp.postprocess_nodes(nodes)


    def _process_colbert(self, nodes, query):
        options = self._get_options('colbertRerank')
        log.debug(f"_process_colbert", options)

        if not options['on']:
            return nodes

        log.debug(f"_process_colbert", self._remove_on(options))
        reranker = ColbertRerank(**self._remove_on(options))
        query_bundle = QueryBundle(query)

        log.info(f"pipeline.py _process_colbert: top_n of {options['top_n']} applied")
        return reranker.postprocess_nodes(nodes, query_bundle)


    def _process_reorder(self, nodes):
        options = self._get_options('longContextReorder')

        if not options['on']:
            return nodes

        reorder = LongContextReorder()

        log.info(f"pipeline.py _process_reorder: executed (no options)")
        return reorder.postprocess_nodes(nodes)


    def _get_options(self, module):
        return self._config['postprocessing'][module]


    def _remove_on(self, options_dict):
        copy = options_dict.copy()
        del copy['on']
        return copy



    # Misc helpers

    def _parse_json(self, config_json):
        log.info(f"pipeline.py _parse_json: ", config_json)
        return {
            'id': 'idstring',
            'name': 'configName',
            'knowledgebases': ['kb1', 'kb2'],
            'retrieval': {
                'vector': 'gpt-3.5-turbo',
                'keyword': 'bm25',
                'alpha': 0.7,
            },
            'postprocessing': {
                'similarity': {
                    'on': False,
                    'similarity_cutoff': 0.7
                },
                'colbertRerank': {
                    'on': False,
                    'top_n': 5
                },
                'longContextReorder': {
                    'on': True,
                }
            },
            'generative_model': 'gpt-3.5-turbo',
            'prompt': {
                'on': True,
                'template_str': 'answer the question - {query_str} - in French'
            }
        }

    def _log_nodes(self, nodes):
        for node in nodes:
            log.info(node)



testPipe = Pipeline({"id":"testjson"})
log.info('FINAL RESPONSE: ', testPipe.query('what is the supersecretword?'))
