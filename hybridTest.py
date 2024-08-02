import hybridSearch.search as search

def print_nodes(nodes):
    for node in nodes:
        print(node)


kb_file_path = './tmpfiles/giraffes.pdf'
search.hybrid_write('giraffes', kb_file_path) # only need to do this the first time

query = 'how long are giraffe necks?'

# get nodes
nodes = search.hybrid_get_nodes('giraffes', query, top_k=5)

all_nodes = nodes['keyword'] + nodes['vector']

print_nodes(all_nodes)



