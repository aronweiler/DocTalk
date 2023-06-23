## Run a single chain LLM over a single vector store

import os
import time
import utilities.console_text as console_text
import documents
import shared
import utilities.calculate_timing as calculate_timing
import callback_handlers
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationTokenBufferMemory
from selector import get_llm, get_embedding
import argparse
import shared

def main(llm, embeddings, database_name:str, top_k = 4, search_type = "mmr", search_distance = .5, verbose = False, max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE):  
    db = documents.get_database(embeddings, database_name) 
    
    vectordbkwargs = {"search_distance": search_distance, "k": top_k, "search_type": search_type}

    memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=max_tokens, memory_key="chat_history", return_messages=True, input_key="question", output_key="answer")    
    qa = ConversationalRetrievalChain.from_llm(llm, db.as_retriever(search_kwargs=vectordbkwargs), memory=memory, verbose=verbose, return_source_documents=True, callbacks=[callback_handlers.DebugCallbackHandler()])

    while True:        
        query = input("Query (x to exit): ")

        if query == "x":
            exit()

        # Time it
        start_time = time.time()
                
        # Run the query
        result = qa({"question": query})

        end_time = time.time()

        # print the answer
        console_text.print_green(result['answer'])
        source_docs = "\n".join([f"\t- {os.path.basename(d.metadata['source'])} page {d.metadata['page']}" if 'page' in d.metadata else f"\t- {os.path.basename(d.metadata['source'])}" for d in result["source_documents"]])
        console_text.print_blue("Source documents:\n" + source_docs)
        
        elapsed_time = end_time - start_time

        print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))

def run(run_local:bool, database_name:str, verbose:bool, top_k:int, search_type:str, search_distance:float):    
    print("-------- Running LLM --------")
    print("run_local:", run_local)
    print("database_name:", database_name)
    print("verbose:", verbose)
    print("top_k:", top_k)
    print("search_type: ", search_type)
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
        
    main(llm, embeddings, database_name, top_k, search_type, search_distance, verbose, max_tokens=max_tokens)
      
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--run_open_ai', action='store_true', default=False, help='Use OpenAI vs. local LLM')
parser.add_argument('--database_name', type=str, default="default", help='Database name to use for document storage')
parser.add_argument('--verbose', action='store_true', default=False, help='Verbose mode')
parser.add_argument('--top_k', type=int, default=5, help='Top K value- number of documents or chunks of documents for the LLM to use to answer a question (Note: this can kill performance locally)')
parser.add_argument('--search_distance', type=float, default=0.1, help='Search distance limits the similarity search in the vector database (value should be 0 and 1, lower value indicates a wider search)')
parser.add_argument('--search_type', type=str, default='mmr', help='Search type can be either "similarity", or "mmr". Default is "mmr"')

# Parse the command-line arguments
args = parser.parse_args()

# Call the run() method with parsed arguments
run(run_local=args.run_open_ai == False, database_name=args.database_name, verbose=args.verbose, top_k=args.top_k, search_type=args.search_type, search_distance=args.search_distance)