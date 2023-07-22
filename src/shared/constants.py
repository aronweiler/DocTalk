import os



OFFLOAD_TO_GPU_LAYERS = 10
AI_TEMP = float(0)
MAX_LOCAL_CONTEXT_SIZE = 4096
MAX_OPEN_AI_CONTEXT_SIZE = 4096

## If we split documents in the loader, need to know by how much
SPLIT_DOCUMENT_CHUNK_SIZE = 300
SPLIT_DOCUMENT_CHUNK_OVERLAP = 100
SPLIT_SEPARATORS = ["\n\n", "\n", " ", ""]

SHARED_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SRC_DIRECTORY = os.path.dirname(SHARED_DIRECTORY)
ROOT_DIRECTORY = os.path.dirname(SRC_DIRECTORY)

CHROMA_DIRECTORY = f"{ROOT_DIRECTORY}/data/ChromaDB_{{database_name}}"

# Keeping the output from some runs here, which I use to estimate times for the local llm runs
LLAMA_TIMINGS_FILE = f"{ROOT_DIRECTORY}/timings/llama_print_timings.txt"


