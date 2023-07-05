import shared
from langchain.vectorstores import Chroma


def get_database(embeddings, database_name, collection_name = Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME):

    db = Chroma(
        persist_directory=shared.CHROMA_DIRECTORY.format(database_name=database_name),        
        embedding_function=embeddings,
        client_settings=shared.get_chroma_settings(database_name),
    )

    print(f"There are {len(db.get()['documents'])} chunks in the datastore")

    return db 

def store_embeddings(embeddings, documents, database_name):   

    db = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory=shared.CHROMA_DIRECTORY.format(database_name=database_name),
        client_settings=shared.get_chroma_settings(database_name),
    )

    print("Persisting DB")
    db.persist()
    db = None
