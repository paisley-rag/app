# test files for connecting with AWS DocumentDB instance
- a set of test files to confirm a connection with AWS DocumentDB and vector embedding persistence
- Note:  the LlamaIndex DocDB integration uses `pymongo`
  - when running the various files, there may be errors from the pymongo package, but these do not seem to impact vector storage / retrieval



## to use
- create a `.env` file (can use env.template as a starter)
  - MONGO_URI will come from the AWS Console for DocumentDB
- ensure you download the global-bundle.pem from the AWS Console
- ensure you've run `pipenv shell` in the root project folder



## overview of files
- `test_nodb.py` : will create a VectorStoreIndex from the same files with no persistence
  - note that running this file should give you a 'baseline' of how llamaIndex will perform
  - note also that since being first created, it appears an underlying LangChain method has changed and is now deprecated (as of Jul 21, 2024)

- `store_vectors.py` : this will vectorize the same files and store the index in DocDB

- `list_vectors.py` : this program queries the contents of the 'testdb', 'testcollection' directly and prints the values to screen
  - note: you can pipe the output to a file to examine output more closely
    - e.g., `python list_vectors.py > output.txt`

- `load_vectors.py` : this will load the vector embeddings from DocDB and then run a query against them

