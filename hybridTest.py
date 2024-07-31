import hybridSearch.search as search

def print_nodes(nodes):
    for node in nodes:
        print(node)



# search.vector_write('./tmpfiles') # only need to do this the first time

query = 'tell me about promises'

# get nodes
nodes = search.hybrid_get_nodes('kb3', query, top_k=5)

all_nodes = nodes['keyword'] + nodes['vector']

print_nodes(all_nodes)



