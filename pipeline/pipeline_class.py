""" Contains Pipeline class, can be executed for testing """

import os

from llama_index.core import get_response_synthesizer, QueryBundle
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LongContextReorder
from llama_index.postprocessor.colbert_rerank import ColbertRerank
from llama_index.core.response_synthesizers import  ResponseMode

import db.app_logger as log
from db.pipeline.hybrid_search import search
import db.pipeline.mongo_util as mg

class Pipeline:
    """

    Pipeline class used to create a RAG pipeline from JSON config file
    - exposes a "query" method to run user queries

    """

    def __init__(self, config_id):
        self._config = self._get_config(config_id)

    def _get_config(self, config_id):
        result = mg.get_one_pipeline(config_id)
        log.info('pipeline.py _get_config', result)
        return result

    def query(self, user_query):
        try:
            pipeline_data = self._pipeline(user_query)
            synthesizer = pipeline_data['synthesizer']
            nodes = pipeline_data['nodes']
            
            # synthesizer, nodes = self._pipeline(user_query).values()
            log.info('nodes:', nodes)

            # Note: if we pass in a `simple template` kwarg here,
            # I believe we can incorporate the custom prompt from 
            # the pipeline config
            return synthesizer.synthesize(user_query, nodes=nodes)
        except Exception as err:
            log.error('pipeline.py query: ******** ERROR *********', type(err), err)


    def _pipeline(self, user_query):
        # get a retriever from each knowledge base
        retrievers = self._process_kbs(self._config['knowledge_bases'])

        log.info('pipeline.py _pipeline: retrievers returned')

        # query each knowledge base and get returned_nodes
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
        return { 'synthesizer': synth, 'nodes': all_nodes }
        # return { 'synthesizer': synth, 'nodes': nodes_reorder }


    # Knowledge base methods
    def _process_kbs(self, kb_ids):
        log.debug(f"pipeline.py _process_kbs: kb_ids {kb_ids}")
        retrievers = list(map(self._get_retriever, kb_ids))

        log.info(f"pipeline.py _process_kbs: returned {len(retrievers)} retrievers", retrievers)
        return retrievers


    def _get_retriever(self, kb_id):

        # result = self._check_kb(kb_id)
        # if not result:
        #     raise Exception(f'Knowledge base id "{kb_id}" not found!')

        # log.info(f"pipeline.py _get_retriever: {kb_id} received")
 
        # just return existing knowledge bases for testing
        vector_retriever = search.vector_retriever(kb_id)
        keyword_retriever = search.keyword_retriever(kb_id)

        log.info("pipeline.py _get_retriever: vector ", vector_retriever, "keyword ", keyword_retriever)
        return { 'vector': vector_retriever, 'keyword': keyword_retriever }


    # Retrieval methods
    def _query_retriever(self, retrievers, user_query):
        nodes = []
        for obj in retrievers:
            log.info('pipeline.py _query_retriever: vector', obj['vector'])
            nodes += obj['vector'].retrieve(user_query)
            log.info('pipeline.py _query_retriever: keyword', obj['keyword'])
            nodes += obj['keyword'].retrieve(user_query)

        return nodes

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
        options = self._get_options('colbert_rerank')
        log.debug("_process_colbert", options)

        if options['on'] != 'True':
            return nodes

        log.debug("_process_colbert", self._remove_on(options))
        reranker = ColbertRerank(**self._remove_on(options))
        query_bundle = QueryBundle(query)

        log.info(f"pipeline.py _process_colbert: top_n of {options['top_n']} applied")
        return reranker.postprocess_nodes(nodes, query_bundle)


    def _process_reorder(self, nodes):
        options = self._get_options('long_context_reorder')
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

    # Misc helpers

    def _log_nodes(self, nodes):
        for node in nodes:
            log.info(node)



    # def _check_kb(self, kb_id):
        
    #     ##############################
    #     result = mg.get(
    #         os.environ['CONFIG_DB'],
    #         os.environ['CONFIG_KB_COL'],
    #         {'id': kb_id}
    #     )
    #     log.info('pipeline.py _check_kb', result)
    #     return result


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


# for direct testing
if __name__ == '__main__':
    testPipe = Pipeline('giraffe2')
    log.info('FINAL RESPONSE: ', testPipe.query('how long are giraffe necks?'))
