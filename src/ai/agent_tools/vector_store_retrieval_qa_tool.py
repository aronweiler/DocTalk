import time
import logging
import os
from typing import Any, Dict, List, Union
import shared.constants as constants
from documents.vector_database import get_database
from shared.selector import get_llm, get_embedding
from langchain.chains import RetrievalQA
import utilities.calculate_timing as calculate_timing
from ai.agent_tools.utilities.abstract_tool import AbstractTool

class VectorStoreRetrievalQATool(AbstractTool):

    def configure(self, memory=None, override_llm=None, json_args:dict={}):
            self.run_locally:bool = bool(json_args["run_locally"])
            self.database_name = json_args["database_name"]
            self.top_k = json_args["top_k"]
            self.search_type = json_args["search_type"]
            self.chain_type = json_args["chain_type"]
            self.search_distance = json_args["search_distance"]
            self.verbose = json_args["verbose"]
            self.max_tokens = json_args["max_tokens"]
            self.return_source_documents = json_args["return_source_documents"]

            # Load the specified database 
            self.db = get_database(get_embedding(self.run_locally), self.database_name)    

            vectordbkwargs = {"search_distance": self.search_distance, "k": self.top_k, "search_type": self.search_type}

            # Get the llm
            if override_llm != None:
                 llm = override_llm
            else:
                llm = get_llm(self.run_locally)
            
            self.retrieval_qa = RetrievalQA.from_chain_type(llm=llm, chain_type=self.chain_type, retriever=self.db.as_retriever(search_kwargs=vectordbkwargs), verbose=self.verbose, return_source_documents=self.return_source_documents)

            logging.debug(f"VectorStoreRetrievalQATool initialized with database_name={self.database_name}, top_k={self.top_k}, search_type={self.search_type}, search_distance={self.search_distance}, verbose={self.verbose}, max_tokens={self.max_tokens}")

    @property
    def database(self):
        return self.db

    def run(self, query:str) -> str:
        logging.debug(f"\nVectorStoreRetrievalQATool got: {query}")

        start_time = time.time()
        result = self.retrieval_qa({"query": query})
        end_time = time.time()
      
        elapsed_time = end_time - start_time
        logging.debug("Operation took: " + calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))

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