import os
import shared
from document_loader import get_database
from selector import get_llm, get_embedding
from langchain.chains import RetrievalQA

class OpenAIVectorStoreTool:

    def __init__(self, database_name, top_k = 4, search_type = "mmr", search_distance = .5, verbose = False, max_tokens = shared.MAX_LOCAL_CONTEXT_SIZE, return_source_documents = False):
            self.database_name = database_name
            self.top_k = top_k
            self.search_type = search_type
            self.search_distance = search_distance
            self.verbose = verbose
            self.max_tokens = max_tokens
            self.return_source_documents = return_source_documents

            # Load the specified database using non-local embeddings
            db = get_database(get_embedding(False), database_name)    

            vectordbkwargs = {"search_distance": search_distance, "k": top_k, "search_type": search_type}

            # Get the open ai llm
            llm = get_llm(False)
            
            self.retrieval_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever(search_kwargs=vectordbkwargs), verbose=verbose, return_source_documents=return_source_documents)           

            print(f"OpenAIVectorStoreTool initialized with database_name={database_name}, top_k={top_k}, search_type={search_type}, search_distance={search_distance}, verbose={verbose}, max_tokens={max_tokens}")

    def run(self, query:str) -> str:
        print("OpenAIVectorStoreTool got: ", query)
        
        result = self.retrieval_qa({"query": query})
        result_string = result['result']

        if self.return_source_documents:
            # Append the source docs to the result, since we can't return anything else but a string??  langchain... more like lamechain, amirite??
            source_docs_list = [f"\t- {os.path.basename(d.metadata['source'])} page {d.metadata['page']}" if 'page' in d.metadata else f"\t- {os.path.basename(d.metadata['source'])}" for d in result["source_documents"]]
            unique_list = list(set(source_docs_list))
            unique_list.sort()
            source_docs = "\n".join(unique_list)
            result_string = result_string + "\n" + source_docs

        return result_string