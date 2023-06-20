import os

from chromadb.config import Settings

OFFLOAD_TO_GPU_LAYERS = 40
AI_TEMP = 0
MAX_LOCAL_CONTEXT_SIZE = 2048

## If we split documents in the loader, need to know by how much
SPLIT_DOCUMENT_CHUNK_SIZE = 1000
SPLIT_DOCUMENT_CHUNK_OVERLAP = 200

APP_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CHROMA_DIRECTORY = f"{APP_DIRECTORY}/ChromaDB_work_design_docs"

# Keeping the output from some runs here, which I use to estimate times for the local llm runs
LLAMA_TIMINGS_FILE = f"{APP_DIRECTORY}/timings/llama_print_timings.txt"

LOCAL_MODEL_PATH = "/Repos/LLM/WizardLM-13B-1.0.ggmlv3.q5_1.bin"
#LOCAL_MODEL_PATH = "/Repos/LLM/open-llama-7B-open-instruct.ggmlv3.q4_1.bin"

CHROMA_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=CHROMA_DIRECTORY,
        anonymized_telemetry=False
    )





