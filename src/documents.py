from shared import (CHROMA_DIRECTORY, CHROMA_SETTINGS, get_embedding)

# probably don't need langchain here, but I might still use it
from langchain.vectorstores import Chroma

def get_documents(db, query, top_k):
    # Trying different ways to get the best starting list of documents    
    docs = db.similarity_search_with_relevance_scores(query, top_k)     
    top_k_results = [d[0] for d in docs]

    return top_k_results

def get_database():
    embeddings = get_embedding()

    db = Chroma(
        persist_directory=CHROMA_DIRECTORY,
        embedding_function=embeddings,
        client_settings=CHROMA_SETTINGS,
    )

    print(f"There are {len(db.get())} documents in the datastore")

    return db 