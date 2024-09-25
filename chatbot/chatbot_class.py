"""
Defines Chatbot class
- previously called "Pipeline" (used interchangeably in code base)
"""

from llama_index.core import get_response_synthesizer, QueryBundle, PromptTemplate
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LongContextReorder
from llama_index.postprocessor.colbert_rerank import ColbertRerank
from llama_index.core.response_synthesizers import  ResponseMode

from db.db.mongo import Mongo
import db.app_logger as log
from db.config import settings

class Chatbot:
    """
    Chatbot class used to create a RAG chatbot from JSON config file
    - exposes a "query" method to run user queries
    """

    def __init__(self, config_id, db: Mongo):
        self._db = db
        self._config = self._get_config(config_id)

    def _get_config(self, config_id):
        result = self._db.get_one_chatbot(config_id)
        log.info('chatbot_class.py _get_config', result)
        return result

    def query(self, user_query):
        try:
            synthesizer, nodes = self._chatbot(user_query).values()
            log.info('chatbot_class.py returned nodes:')
            self._log_nodes(nodes)

            return synthesizer.synthesize(user_query, nodes=nodes)
        except Exception as err:
            log.error('chatbot_class.py query: ******** ERROR *********', type(err), err)
            return {
                "response": None,
                "source_nodes": [],
                "metadata": {}
            }


    def _chatbot(self, user_query):
        # get a retriever from each knowledge base
        retrievers = self._process_kbs(self._config['knowledge_bases'])

        log.info('chatbot_class.py _chatbot: retrievers returned')

        # query each knowledge base and get returned_nodes
        vector_nodes, keyword_nodes  = self._query_retriever(retrievers, user_query).values()
        all_nodes = vector_nodes + keyword_nodes

        log.info("chatbot_class.py _chatbot: all_nodes")
        self._log_nodes(all_nodes)

        # post-processing of nodes
        nodes_similar = self._process_similarity(all_nodes)

        log.info('nodes_similar')
        self._log_nodes(nodes_similar)

        nodes_rerank = self._process_colbert(nodes_similar, user_query)

        log.info('nodes_rerank')
        self._log_nodes(nodes_rerank)

        nodes_reorder = self._process_reorder(nodes_rerank)

        log.info('nodes_reorder')
        self._log_nodes(nodes_reorder)

        # return appropriate synthesizer
        synth = self._process_prompt()

        return { 'synthesizer': synth, 'nodes': nodes_reorder }


    # Knowledge base methods
    def _process_kbs(self, kb_ids):
        log.debug(f"chatbot_class.py _process_kbs: kb_ids {kb_ids}")
        retrievers = list(map(self._get_retriever, kb_ids))

        log.info(f"chatbot_class.py _process_kbs: returned retrievers from {len(retrievers)} kbs",
                 retrievers)
        return retrievers


    def _get_retriever(self, kb_id):
        log.info('chatbot_class.py _get_retriever START')
        vector_retriever = self._db.get_vector_retriever(kb_id, settings.DEFAULT_TOP_K)
        log.info('chatbot_class.py _get_retriever max_top_k', self._max_top_k(kb_id))
        keyword_retriever = self._db.get_keyword_retriever(kb_id, self._max_top_k(kb_id))

        log.info("chatbot_class.py _get_retriever: vector ", vector_retriever,
                 "keyword ", keyword_retriever)
        return { 'vector': vector_retriever, 'keyword': keyword_retriever }


    # Retrieval methods
    def _query_retriever(self, retrievers, user_query):
        vector_nodes = []
        keyword_nodes = []
        for obj in retrievers:
            # vector retrieval
            log.info('chatbot_class.py _query_retriever: vector', obj['vector'])
            new_nodes = obj['vector'].retrieve(user_query)
            vector_nodes += new_nodes
            log.info('chatbot_class.py _query_retriever',
                     f'returned {len(new_nodes)} vector nodes')

            # keyword retrieval
            log.info('chatbot_class.py _query_retriever: keyword', obj['keyword'])
            new_nodes = obj['keyword'].retrieve(user_query)
            keyword_nodes += new_nodes
            log.info('chatbot_class.py _query_retriever',
                     f'returned {len(new_nodes)} keyword nodes')

            log.info('chatbot_class.py _query_retriever: both retrievers successfully queried')

        log.info('chatbot_class.py _query_retriever', 'vector_nodes', vector_nodes)
        log.info('chatbot_class.py _query_retriever', 'keyword_nodes', keyword_nodes)
        return { "vector_nodes": vector_nodes, "keyword_nodes": keyword_nodes }

    def _process_similarity(self, nodes):
        options = self._config['similarity']

        if options["on"]:
            log.info("chatbot_class.py _process_similarity: similarity on")
            similarity_pp = SimilarityPostprocessor(**self._remove_on(options))
            return similarity_pp.postprocess_nodes(nodes)

        log.info("chatbot_class.py _process_similarity: similarity off")
        return nodes

    def _process_colbert(self, nodes, query):
        options = self._config['colbert_rerank']
        log.debug("_process_colbert", options)

        if options['on']:
            log.info("chatbot_class.py _process_colbert: colbert rerank on")
            reranker = ColbertRerank(**self._remove_on(options))
            query_bundle = QueryBundle(query)
            log.info(f"chatbot_class.py _process_colbert: top_n of {options['top_n']} applied")
            return reranker.postprocess_nodes(nodes, query_bundle)

        log.info("chatbot_class.py _process_colbert: colbert rerank off")
        return nodes

    def _process_reorder(self, nodes):
        options = self._config['long_context_reorder']
        if options['on']:
            reorder = LongContextReorder()
            log.info("chatbot_class.py _process_reorder: long context reorder on")
            return reorder.postprocess_nodes(nodes)

        log.info("chatbot_class.py _process_reorder: long context reorder off")
        return nodes

    def _process_prompt(self):
        custom_prompt = self._config['prompt']

        synth = self._get_default_synth()

        if custom_prompt:
            log.info("using custom prompts")
            new_template = PromptTemplate(self._config['prompt'])
            synth.update_prompts(
                {"text_qa_template": new_template}
            )
        else:
            log.info("no custom prompts")

        prompt = synth.get_prompts()
        self._log_prompt(prompt)
        return synth

    def _get_default_synth(self):
        synth = get_response_synthesizer(
            response_mode=ResponseMode.SIMPLE_SUMMARIZE
        )
        return synth

    def _remove_on(self, options_dict):
        copy = options_dict.copy()
        del copy['on']
        return copy

    # Misc helpers

    def _log_nodes(self, nodes):
        for node in nodes:
            log.info(node)


    def _log_prompt(self, prompts_dict):
        for k, p in prompts_dict.items():
            log.info("Prompt Key: ", k)
            log.info("Text: ", p.get_template())


    def _max_top_k(self, kb_id):
        # kb_id = self._config['id']
        log.info('************** kb_id', kb_id)
        max_nodes = self._db.nodes_in_keyword(kb_id)
        log.info('chatbot_class.py _max_top_k:', f'max_nodes: {max_nodes}')
        if settings.DEFAULT_TOP_K > max_nodes:
            log.info(f'chatbot_class.py _max_top_k: returned max_nodes {max_nodes}')
            return max_nodes

        log.info(f'chatbot_class.py _max_top_k: returned max_nodes {settings.DEFAULT_TOP_K}')
        return settings.DEFAULT_TOP_K


    # Public class method
    @classmethod
    def get_default_prompt(cls):
        '''
        retrieves default prompt for UI / new chatbots
        - used in post /api/chatbots route so all new chatbots have a prompt
        '''
        synth = get_response_synthesizer(
            response_mode=ResponseMode.SIMPLE_SUMMARIZE
        )
        template = synth.get_prompts()['text_qa_template'].get_template()
        return template
