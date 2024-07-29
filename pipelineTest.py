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
