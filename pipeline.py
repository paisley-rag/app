""" Contains Pipeline class, can be executed for testing """

import os

from llama_index.core import get_response_synthesizer, QueryBundle
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LongContextReorder
from llama_index.postprocessor.colbert_rerank import ColbertRerank
from llama_index.core.response_synthesizers import  ResponseMode

import app_logger as log
from hybridSearch import search
import mongo_util as mg

class Pipeline:
    """

    Pipeline class used to create a RAG pipeline from JSON config file
    - exposes a "query" method to run user queries

    """

    def __init__(self, config_id):
        self._config = self._get_config(config_id)

    def query(self, user_query):
        synthesizer, nodes = self._pipeline(user_query).values()
        return synthesizer.synthesize(user_query, nodes=nodes)


    def _pipeline(self, user_query):
        # get a retriever from each knowledge base
        retrievers = self._process_kbs(self._config['knowledgebases'])

        # query each knowledge base and get returned_nodes
        # all_nodes = asyncio.run(self._query_retriever(retrievers, user_query))
        all_nodes = self._query_retriever(retrievers, user_query)

        log.info("pipeline.py _pipeline: all_nodes")
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
        log.debug(f"pipeline.py _process_kbs: kb_ids {kb_ids}")
        retrievers = list(map(self._get_retriever, kb_ids))

        log.info(f"pipeline.py _process_kbs: returned {len(retrievers)} retrievers", retrievers)
        return retrievers


    def _get_retriever(self, kb_id):
        log.info(f"pipeline.py _get_retriever: {kb_id} received")

        # just return existing knowledge bases for testing
        vector_retriever = search.vector_retriever(kb_id)
        keyword_retriever = search.keyword_retriever(kb_id)
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
        log.info("pipeline.py _process_similarity: options", options)
        if options['on'] != 'True':
            return nodes

        log.debug("pipeline.py _process_similarity: ", self._remove_on(options))

        similarity_pp = SimilarityPostprocessor(**self._remove_on(options))
        log.info(
            "pipeline.py _process_similarity: cutoff applied",
            options['similarity_cutoff']
        )
        return similarity_pp.postprocess_nodes(nodes)


    def _process_colbert(self, nodes, query):
        options = self._get_options('colbertRerank')
        log.debug("_process_colbert", options)

        if options['on'] != 'True':
            return nodes

        log.debug("_process_colbert", self._remove_on(options))
        reranker = ColbertRerank(**self._remove_on(options))
        query_bundle = QueryBundle(query)

        log.info(f"pipeline.py _process_colbert: top_n of {options['top_n']} applied")
        return reranker.postprocess_nodes(nodes, query_bundle)


    def _process_reorder(self, nodes):
        options = self._get_options('longContextReorder')

        if options['on'] != 'True':
            return nodes

        reorder = LongContextReorder()

        log.info("pipeline.py _process_reorder: executed (no options)")
        return reorder.postprocess_nodes(nodes)


    def _get_options(self, module):
        return self._config['postprocessing'][module]


    def _remove_on(self, options_dict):
        copy = options_dict.copy()
        del copy['on']
        return copy



    # db helpers

    def _get_config(self, config_id):
        result = mg.get(
            os.environ['CONFIG_DB'],
            os.environ['CONFIG_PIPELINE_COL'],
            {'id': config_id}
        )
        log.info('pipeline.py _get_config', result)
        return result



    # Misc helpers

    def _log_nodes(self, nodes):
        for node in nodes:
            log.info(node)


# for direct testing
if __name__ == '__main__':
    testPipe = Pipeline('giraffe2')
    log.info('FINAL RESPONSE: ', testPipe.query('how long are giraffe necks?'))
