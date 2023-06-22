import os
import argparse
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
    Docx2txtLoader,
    #UnstructuredWordDocumentLoader 
)

import shared
import selector

DOCUMENT_TYPES = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".doc": Docx2txtLoader, #UnstructuredWordDocumentLoader,
    ".docx": Docx2txtLoader
    }

def load_single_document(file_path: str) -> List[Document]:
    # Loads a single document from a file path
    file_extension = os.path.splitext(file_path)[1]
    loader_class = DOCUMENT_TYPES.get(file_extension)
    
    if loader_class:
        loader = loader_class(file_path)
    else:
        raise ValueError(f"Document type is undefined, {file_path}")

    # Should return a list[Document] from within the current file.  For PDFs this looks like a document per page.
    try:
        documents = loader.load()
        return documents
    except:
        err = f"Could not load {file_path}"
        print(err)
        raise(ValueError(err))
    
    

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

def main(document_directory:str, database_name:str, run_local:bool, split_documents:bool, split_chunks:int, split_overlap:int):
    documents = load_documents(document_directory)

    if split_documents:
        text_splitter = RecursiveCharacterTextSplitter(separators=shared.SPLIT_SEPARATORS, chunk_size=split_chunks, chunk_overlap=split_overlap)
        texts = text_splitter.split_documents(documents)
        
        print(f"Split into {len(texts)} chunks of text (chunk_size: {split_chunks}, chunk_overlap: {split_overlap})")
    else:
        texts = documents

    print(f"Loaded {len(documents)} pages of documents from {document_directory}")

    embeddings = selector.get_embedding(run_local)

    db = Chroma.from_documents(
        texts,
        embedding=embeddings,
        persist_directory=shared.CHROMA_DIRECTORY.format(database_name=database_name),
        client_settings=shared.get_chroma_settings(database_name),
    )

    print("Persisting DB")
    db.persist()
    db = None

    
#document_directory = "/repos/sample_docs/P&R"
#document_directory = "/repos/sample_docs/work/fda"
#document_directory = "/Repos/sample_docs/work/design_docs"    
    
if __name__ == '__main__':    
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('--document_directory', type=str, default='/repos/sample_docs/work/design_docs', help='Directory from where documents are ingested')
    parser.add_argument('--database_name', type=str, default='default', help='Name of the ChromaDB to store documents in')
    parser.add_argument('--run_open_ai', action='store_true', default=False, help='Use OpenAI vs. local embeddings')
    parser.add_argument('--split_documents', action='store_true', default=False, help='Split documents?')
    parser.add_argument('--split_chunks', type=int, default=shared.SPLIT_DOCUMENT_CHUNK_SIZE, help='Split chunk size')
    parser.add_argument('--split_overlap', type=int, default=shared.SPLIT_DOCUMENT_CHUNK_OVERLAP, help='Split overlap size')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the run() method with parsed arguments
    main(document_directory=args.document_directory, database_name=args.database_name, run_local=args.run_open_ai == False, split_documents=args.split_documents, split_chunks=args.split_chunks, split_overlap=args.split_overlap)