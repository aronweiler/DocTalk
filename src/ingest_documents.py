import argparse
from shared.constants import SPLIT_DOCUMENT_CHUNK_OVERLAP, SPLIT_DOCUMENT_CHUNK_SIZE
from documents.document_loader import main

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('--document_directory', type=str, required=True, help='Directory from where documents are ingested')
    parser.add_argument('--database_name', type=str, default='default', help='Name of the ChromaDB to store documents in')
    parser.add_argument('--run_open_ai', action='store_true', default=False, help='Use OpenAI vs. local embeddings')
    parser.add_argument('--split_documents', action='store_true', default=False, help='Split documents?')
    parser.add_argument('--split_chunks', type=int, default=SPLIT_DOCUMENT_CHUNK_SIZE, help='Split chunk size')
    parser.add_argument('--split_overlap', type=int, default=SPLIT_DOCUMENT_CHUNK_OVERLAP, help='Split overlap size')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the run() method with parsed arguments
    main(document_directory=args.document_directory, database_name=args.database_name, run_local=args.run_open_ai == False, split_documents=args.split_documents, split_chunks=args.split_chunks, split_overlap=args.split_overlap)