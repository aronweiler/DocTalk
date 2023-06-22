from selector import get_llm, get_embedding
import run_llm_langchain
import argparse
import shared

def run(run_local:bool, database_name:str, verbose:bool, top_k:int, search_distance:float):    
    print("-------- Running LLM --------")
    print("run_local:", run_local)
    print("database_name:", database_name)
    print("verbose:", verbose)
    print("top_k:", top_k)
    print("search_distance:", search_distance)
    print("-----------------------------")
    
    if run_local:    
        llm = get_llm(True)
        embeddings = get_embedding(True)
        max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE
    else:
        llm = get_llm(False)
        embeddings = get_embedding(False)
        max_tokens = shared.MAX_OPEN_AI_CONTEXT_SIZE
        
    run_llm_langchain.main(llm, embeddings, database_name, top_k, search_distance, verbose, max_tokens=max_tokens)
      
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--run_open_ai', action='store_true', default=False, help='Use OpenAI vs. local LLM')
parser.add_argument('--database_name', type=str, default="default", help='Database name to use for document storage')
parser.add_argument('--verbose', action='store_true', default=False, help='Verbose mode')
parser.add_argument('--top_k', type=int, default=5, help='Top K value- number of documents or chunks of documents for the LLM to use to answer a question (Note: this can kill performance locally)')
parser.add_argument('--search_distance', type=float, default=0.1, help='Search distance limits the similarity search in the vector database (value should be 0 and 1, lower value indicates a wider search)')

# Parse the command-line arguments
args = parser.parse_args()

# Call the run() method with parsed arguments
run(run_local=args.run_open_ai == False, database_name=args.database_name, verbose=args.verbose, top_k=args.top_k, search_distance=args.search_distance)