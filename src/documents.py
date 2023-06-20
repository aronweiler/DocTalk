from shared import (CHROMA_DIRECTORY, CHROMA_SETTINGS)
from selector import get_embedding

# probably don't need langchain here, but I might still use it
from langchain.vectorstores import Chroma

def get_documents(db:Chroma, query, top_k):
    # Trying different ways to get the best starting list of documents    
    return db.similarity_search(query, top_k)     
    
    #if I use similarity_search_with_relevance_scores or something else that will return a tuple
    # top_k_results = [d[0] for d in docs]
    # return top_k_documents

def get_database(local):
    embeddings = get_embedding(local)

    db = Chroma(
        persist_directory=CHROMA_DIRECTORY,
        embedding_function=embeddings,
        client_settings=CHROMA_SETTINGS,
    )

    print(f"There are {len(db.get()['documents'])} documents in the datastore")

    return db 

# db = get_database()
# results = get_documents(db, "Summarize the meeting that took place on February 17, 2022", 5)
