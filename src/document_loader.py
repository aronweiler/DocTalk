import os
import multiprocessing
from typing import List

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import (Chroma)
from langchain.document_loaders import (
    CSVLoader,    
    PyPDFLoader,    
    TextLoader,
    Docx2txtLoader    
)

import shared
import selector

DOCUMENT_TYPES = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".doc": Docx2txtLoader,
    ".docx": Docx2txtLoader
    }

def load_single_document(file_path: str) -> List[Document]:
    # Loads a single document from a file path
    file_extension = os.path.splitext(file_path)[1]
    loader_class = DOCUMENT_TYPES.get(file_extension)
    
    if loader_class:
        loader = loader_class(file_path)
    else:
        raise ValueError("Document type is undefined")

    # Should return a list[Document] from within the current file.  For PDFs this looks like a document per page.
    return loader.load()
    # I think privateGPT was doing the loader.load()[0], but that wasn't working for me. 
    # if file_extension == ".pdf":
    #     return loader.load_and_split()
    # else:
    #     return loader.load()[0]
    

def load_document_batch(filepaths):
    print("Loading document batch")
    # create a thread pool
    with ThreadPoolExecutor(len(filepaths)) as exe:
        # load files
        futures = [exe.submit(load_single_document, name) for name in filepaths]
        # collect data
        data_list = [future.result() for future in futures]
        # return data and file paths
        return (data_list, filepaths)

def load_documents(source_dir: str) -> List[Document]:
    # Loads all documents from the source documents directory
    all_files = os.listdir(source_dir)
    paths = []
    for file_path in all_files:
        file_extension = os.path.splitext(file_path)[1]
        source_file_path = os.path.join(source_dir, file_path)
        if file_extension in DOCUMENT_TYPES.keys():
            paths.append(source_file_path)

    num_processors = multiprocessing.cpu_count()
    n_workers = min(num_processors, len(paths))
    chunksize = round(len(paths) / n_workers)
    docs = []
    with ProcessPoolExecutor(n_workers) as executor:
        futures = []
        # split the load operations into chunks
        for i in range(0, len(paths), chunksize):
            # select a chunk of filenames
            filepaths = paths[i:(i + chunksize)]
            # submit the task
            future = executor.submit(load_document_batch, filepaths)
            futures.append(future)
        # process all results
        for future in as_completed(futures):
            # open the file and load the data
            contents, _ = future.result()
            
            if type(contents) == list:
                for doc in contents[0]:
                    docs.append(doc)
            else:
                docs.extend(contents)

    return docs

def main(document_directory:str, run_local, split_documents):
    """ document_directory: Directory to load documents from
    split_documents: Should documents be split into chunks?  """
    documents = load_documents(document_directory)

    if split_documents:
        text_splitter = RecursiveCharacterTextSplitter(separators=["\r\n", "\n\n", "\n"], chunk_size=shared.SPLIT_DOCUMENT_CHUNK_SIZE, chunk_overlap=shared.SPLIT_DOCUMENT_CHUNK_OVERLAP)
        texts = text_splitter.split_documents(documents)
    else:
        texts = documents

    print(f"Loaded {len(documents)} pages of documents from {document_directory}")
    
    if split_documents:
        print(f"Split into {len(texts)} chunks of text (chunk_size: {shared.SPLIT_DOCUMENT_CHUNK_SIZE}, chunk_overlap: {shared.SPLIT_DOCUMENT_CHUNK_OVERLAP})")

    embeddings = selector.get_embedding(run_local)

    db = Chroma.from_documents(
        texts,
        embedding=embeddings,
        persist_directory=shared.CHROMA_DIRECTORY,
        client_settings=shared.CHROMA_SETTINGS,
    )

    print("Persisting DB")
    db.persist()
    db = None

if __name__ == "__main__":
    #document_directory = "/repos/sample_docs/P&R"
    #document_directory = "/repos/sample_docs/work/fda"
    document_directory = "/Repos/sample_docs/work/design_docs"

    split_documents = input("Do you want to split loaded documents? (Y/N): ").upper() == "Y"

    print()
    print("Select the embeddings you want to use:")
    print("1: HuggingFaceInstructEmbeddings")
    print("2: OpenAIEmbeddings")
    
    embedding_selection = input("Enter your selection: ")

    if embedding_selection == "1":
        main(document_directory=document_directory, run_local=True, split_documents=split_documents)
    else:
        main(document_directory=document_directory, run_local=False, split_documents=split_documents)
    