import shared
from langchain.vectorstores import Chroma

def get_documents(db:Chroma, query, top_k):
    # Trying different ways to get the best starting list of documents    
    return db.similarity_search(query, top_k)     
    
    #if I use similarity_search_with_relevance_scores or something else that will return a tuple
    # top_k_results = [d[0] for d in docs]
    # return top_k_documents

def get_database(embeddings, database_name):

    db = Chroma(
        persist_directory=shared.CHROMA_DIRECTORY.format(database_name=database_name),
        embedding_function=embeddings,
        client_settings=shared.get_chroma_settings(database_name),
    )

    print(f"There are {len(db.get()['documents'])} chunks in the datastore")

    return db 
