from llama_index.core import QueryBundle
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LongContextReorder
from llama_index.postprocessor.colbert_rerank import ColbertRerank

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


