import os

from chromadb.config import Settings

from langchain.document_loaders import (
    CSVLoader,    
    PyPDFLoader,    
    TextLoader,
    Docx2txtLoader    
)

MAX_LOCAL_CONTEXT_SIZE = 2048

## Should we split documents?  By how much?
SPLIT_DOCUMENTS = True
SPLIT_DOCUMENT_CHUNK_SIZE = 1300
SPLIT_DOCUMENT_CHUNK_OVERLAP = 200

APP_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DOCUMENT_DIRECTORY = "/repos/sample_docs/P&R"
CHROMA_DIRECTORY = f"{APP_DIRECTORY}/ChromaDB"
LLAMA_TIMINGS_FILE = f"{APP_DIRECTORY}/timings/llama_print_timings.txt"

LOCAL_MODEL_PATH = "/Repos/LLM/WizardLM-13B-1.0.ggmlv3.q5_1.bin"
#LOCAL_MODEL_PATH = "/Repos/LLM/open-llama-7B-open-instruct.ggmlv3.q4_1.bin"

DOCUMENT_TYPES = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".doc": Docx2txtLoader,
    ".docx": Docx2txtLoader
    }

CHROMA_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=CHROMA_DIRECTORY,
        anonymized_telemetry=False
    )





