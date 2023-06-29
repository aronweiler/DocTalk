import time
import os
import shared
from document_loader import get_database
from selector import get_llm, get_embedding
from langchain.chains import RetrievalQA
from langchain.prompts import Prompt
import utilities.calculate_timing as calculate_timing

class VectorStoreRetrievalQATool:

    def __init__(self, memory, database_name, run_locally, top_k = 4, chain_type="stuff", search_type = "mmr", search_distance = .5, verbose = False, max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE, return_source_documents = False, return_direct = None):
            self.database_name = database_name
            self.top_k = top_k
            self.search_type = search_type
            self.search_distance = search_distance
            self.verbose = verbose
            self.max_tokens = max_tokens
            self.return_source_documents = return_source_documents

            # Load the specified database 
            db = get_database(get_embedding(run_locally), database_name)    

            vectordbkwargs = {"search_distance": search_distance, "k": top_k, "search_type": search_type}

            # Get the llm
            llm = get_llm(run_locally)
            
            self.retrieval_qa = RetrievalQA.from_chain_type(llm=llm, chain_type=chain_type, retriever=db.as_retriever(search_kwargs=vectordbkwargs), verbose=verbose, return_source_documents=return_source_documents)

            print(f"VectorStoreRetrievalQATool initialized with database_name={database_name}, top_k={top_k}, search_type={search_type}, search_distance={search_distance}, verbose={verbose}, max_tokens={max_tokens}")

    def run(self, query:str) -> str:
        print(f"\nVectorStoreRetrievalQATool got: {query}")

        start_time = time.time()
        result = self.retrieval_qa({"query": query})
        end_time = time.time()
      
        elapsed_time = end_time - start_time
        print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))

        result_string = result['result']

        # When this tool is used from the self_ask_agent_tool, it doesn't 
        if self.return_source_documents:
            # Append the source docs to the result, since we can't return anything else but a string??  langchain... more like lamechain, amirite??
            source_docs_list = [f"\t- {os.path.basename(d.metadata['source'])} page {int(d.metadata['page']) + 1}" if 'page' in d.metadata else f"\t- {os.path.basename(d.metadata['source'])}" for d in result["source_documents"]]
            unique_list = list(set(source_docs_list))
            unique_list.sort()
            source_docs = "\n".join(unique_list)
            result_string = result_string + "\nSource Documents:\n" + source_docs

        return result_string