from llama_index.core import QueryBundle
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LongContextReorder
from llama_index.postprocessor.colbert_rerank import ColbertRerank
from llama_index.core import get_response_synthesizer, PromptTemplate
from llama_index.core.response_synthesizers import ResponseMode

import hybridSearch.search as search

def print_nodes(nodes):
    for node in nodes:
        print(node)


query = 'tell me about promises'

# get all nodes
nodes = search.hybrid_get_nodes(query, top_k=3)
all_nodes = nodes['keyword'] + nodes['vector']


# similarity
similarity_pp = SimilarityPostprocessor(
    nodes=all_nodes,
    similarity_cutoff=0.5
)

nodes_similar = similarity_pp.postprocess_nodes(all_nodes)





# Colbert rerank
reranker = ColbertRerank(top_n=4)
query_bundle = QueryBundle(query)

nodes_rerank = reranker.postprocess_nodes(all_nodes, query_bundle)

print('='*20)
print_nodes(nodes_rerank)



# LongContextReorder
reorder = LongContextReorder()

nodes_reorder = reorder.postprocess_nodes(nodes_rerank)

print('='*20)
print_nodes(nodes_reorder)



# Response synthesizer
synth = get_response_synthesizer(
    response_mode=ResponseMode.SIMPLE_SUMMARIZE
)

response = synth.synthesize(query, nodes=nodes_reorder)
print(response)

print('*'*20)


# Custom Prompt
new_prompt = (
    "Context information is below.\n"
    "-----------------------------\n"
    "{context_str}\n"
    "-----------------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query in French.\n"
    "Query: {query_str}\n"
    "Answer: "
)
new_template = PromptTemplate(new_prompt)

synth.update_prompts(
    {"text_qa_template": new_template}
)

response = synth.synthesize(query, nodes=nodes_reorder)
print(response)





'''
Notes:

incorporate post-processing modules:
- created `pipelineTest.py` based upon ‘hybridTest.py’
- added similarity
- adding ColbertRerank
- found Colbert import statement from https://docs.llamaindex.ai/en/stable/examples/pipeline/query_pipeline_memory/?h=colbertr
- found reranker syntax from https://docs.llamaindex.ai/en/stable/examples/node_postprocessor/LLMReranker-Lyft-10k/?h=reranker
- adding LongContextReorder
- https://docs.llamaindex.ai/en/stable/module_guides/querying/node_postprocessors/node_postprocessors/?h=

- post-processing modules all seem to work
- need to go from nodes to query response now
- llamaindex uses a “response synthesizer”
- https://docs.llamaindex.ai/en/stable/api_reference/response_synthesizers/
- “simple_summarize” merges all text chunks from nodes into 1 and makes an LLM call
- it will fail if the merged text chunk exceeds the context window size

- Accessing and customizing prompts
- https://docs.llamaindex.ai/en/stable/examples/prompts/prompt_mixin/
- `synthesizer.get_prompts()` returns a dictionary of prompts
- key is a template (e.g., “text_qa_template”)
- see promptTest.py to access returned dict and display prompt content
'''