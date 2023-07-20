import os
import time
import json
from typing import List
from documents.vector_database import get_database
from shared.selector import get_llm, get_embedding
from langchain.chains import RetrievalQA
from langchain.prompts import Prompt
import utilities.calculate_timing as calculate_timing
from utilities.token_helper import num_tokens_from_string
from langchain.vectorstores import Chroma
import shared.selector as selector
from langchain.docstore.document import Document
from langchain.retrievers import KNNRetriever
from ai.agent_tools.utilities.abstract_tool import AbstractTool

class VectorStoreSearchTool(AbstractTool):

    def configure(self, database_names, run_locally, return_source_documents):
            self.databases: List[Chroma] = []
            self.return_source_documents = return_source_documents
            self.embedding = get_embedding(run_locally)

            # Load the specified database
            for database_name in database_names:
                self.databases.append(get_database(self.embedding, database_name))

            
    # def run(self, search_terms) -> str:
    #     print(f"\nVectorStoreSearchTool got: {search_terms}\n")

    #     # search_json = json.loads(search_terms)

    #     # date_start = search_json["date_start"]
    #     # date_end = search_json["date_end"]
    #     # search_terms = search_json["search_terms"]

    #     start_time = time.time()
        
    #     chunks = []

    #     # Get all of the chunks that contain this search term        
    #     # for doc in self.db.get()["documents"]:
    #     #     for search_term in search_terms:
    #     #          if search_term in doc:
    #     #             chunks.append(doc)
    #     ## Look at that mess up there...
    #     ## The following list comprehension line is courtesy of ChatGPT lol
    #     # for db in self.databases:
    #     #     chunks.append([doc for doc in db.get()["documents"] if any(search_term in doc for search_term in search_terms)])

    #     doc_details = {}
    #     final_doc_list = []

    #     for db in self.databases:
            
    #         full_docs = {}
    #         relevant_documents = db.similarity_search_with_relevance_scores(search_terms, len(db.get()))            
    #         for doc in relevant_documents:
    #             page_content = doc[0].page_content
    #             chunk = {"source": os.path.basename(doc[0].metadata['source']), "tokens": num_tokens_from_string(page_content), "score": doc[1]}
    #             chunks.append(chunk)
    #             source = os.path.basename(doc[0].metadata['source'])
    #             # is it already in there?
    #             if source in doc_details:
    #                 # Append this token count
    #                 doc_details[source] = num_tokens_from_string(page_content) + doc_details[source] #f"{doc_details[source]}\n{doc[0].page_content}"
    #                 full_docs[source] = page_content + "\n" + full_docs[source]
    #             else:
    #                 # Create new
    #                 doc_details[source] = num_tokens_from_string(page_content)
    #                 full_docs[source] = page_content

    #         documents:List[Document] = []
    #         for source in full_docs.keys():            
    #             content:str = full_docs[source]
    #             documents.append(Document(page_content=content, metadata={"source": source}))

    #         temp_db = Chroma.from_documents(
    #             documents,
    #             embedding=self.embedding,
    #         )
                 
    #         knn_retriever = KNNRetriever.from_texts([d for d in full_docs.values()], self.embedding, k=len(temp_db.get()["documents"]))
    #         knn_docs = knn_retriever.get_relevant_documents(search_terms)
    #         rel_docs = temp_db.similarity_search_with_relevance_scores(search_terms, len(temp_db.get()["documents"]))
    #         final_doc_list.append(rel_docs)

    #     total_relevance_scores = {}
    #     for db_harvest in final_doc_list:
    #          for doc in db_harvest:
    #             total_relevance_scores[doc[0].metadata['source']] = doc[1]

    #         #print(len(doc_details))

    #         # relevant_documents = db.similarity_search_with_relevance_scores(search_terms, len(db.get()["documents"]))  

    #     # for doc in doc_details.keys():
    #     #     num_tokens_from_string(doc_details[doc])

    #     ## TODO: Add metadata (source docs) to return values
    #     # if self.return_source_documents:

    #     # create a string I can pass back
    #     chunk_list = list(chunks)
    #     unique_sources = set([chunk["source"] for chunk in chunk_list])

    #     sorted_list = sorted(
    #         [{'source': c, 'tokens': doc_details[c], 'relevance_score': total_relevance_scores[c]} for c in unique_sources],
    #         key=lambda x: x['relevance_score'],
    #         reverse=True
    #     )

    #     result = {
    #         "related_document_count": len(set([chunk["source"] for chunk in chunk_list])),            
    #         "sources": sorted_list#[{'source': c, 'tokens': doc_details[c], 'relevance_score': total_relevance_scores[c]} for c in unique_sources]
    #     }

    #     end_time = time.time()
      
    #     elapsed_time = end_time - start_time
    #     print("Operation took: ", calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))

    #     # TODO: Return JSON
    #     return json.dumps(result)
    

    def run(self, search_terms):
        print(f"\nVectorStoreSearchTool got: {search_terms}\n")

        for db in self.databases:            
            print("For database: ", db._persist_directory)
            relevant_documents = db.similarity_search_with_relevance_scores(search_terms, 9999999)
            print(f"Found {len(relevant_documents)} chunks of related documents")
            # Print out the max relevance score from the relevant documents
            print(f"Max relevance score: {max(relevant_documents, key=lambda x: x[1])[1]}")
            # Print out the min relevance score from the relevant documents
            print(f"Min relevance score: {min(relevant_documents, key=lambda x: x[1])[1]}")

            # Sum the [0].page_content of each item in relevant_documents
            print(f"Sum of page content: {sum([len(x[0].page_content) for x in relevant_documents])}")
            

# import sys
# import os

# # Get the parent directory path
# parent_dir = os.path.dirname(os.path.abspath(__file__))

# # Add the parent directory to sys.path
# sys.path.insert(0, parent_dir)

searcher = VectorStoreSearchTool(["pr_meeting_minutes"], False, False)    
result = searcher.run("Comments or motions by Rene Smith")
print(result)