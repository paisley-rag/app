from hybridSearch import keyword
from hybridSearch import vector

# defaults
default_top_k = 5

# keyword
def keyword_write(file_path):
    keyword.write_to_db(file_path)

def keyword_query(query, top_k=default_top_k):
    retriever = keyword.get_retriever(top_k=top_k)
    nodes = retriever.retrieve(query)

    for node in nodes:
        print(node)

def keyword_retriever(top_k=default_top_k):
    return keyword.get_retriever(top_k=top_k)


# vector
def vector_write(file_path):
    vector.write_to_db(file_path)


def vector_query(query, top_k=default_top_k):
    retriever = vector.get_retriever(top_k=top_k)
    nodes = retriever.retrieve(query)

    for node in nodes:
        print(node)

def vector_retriever(top_k=default_top_k):
    return vector.get_retriever(top_k=top_k)


# hybrid

def hybrid_write(file_path):
    keyword.write_to_db(file_path)
    vector.write_to_db(file_path)


def hybrid_get_nodes(query, top_k=default_top_k):
    vector_retriever = vector.get_retriever(top_k=top_k)
    keyword_retriever = keyword.get_retriever(top_k=top_k)

    vector_nodes = vector_retriever.retrieve(query)
    keyword_nodes = keyword_retriever.retrieve(query)

    return { 'keyword': keyword_nodes, 'vector': vector_nodes }

