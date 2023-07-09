import os
import callback_handlers

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationTokenBufferMemory

from shared.selector import get_embedding, get_llm
from documents.vector_database import get_database

from ai.qa_chain_configuration import QAChainConfiguration
from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult

class QAChainAI(AbstractAI):

    def configure(self, json_args) -> None:
        configuration = QAChainConfiguration(json_args)
        embeddings = get_embedding(configuration.run_locally)    
        db = get_database(embeddings, configuration.database_name) 
        llm = get_llm(configuration.run_locally, float(configuration.ai_temp))
        
        memory = self._get_memory(llm, configuration.max_tokens) if configuration.use_memory else None    
        
        self.qa_chain = self._get_chain(llm, memory, db, configuration.top_k, configuration.chain_type, configuration.search_type, configuration.search_distance, configuration.verbose)


    def _get_chain(self, llm, memory, db, top_k, chain_type, search_type, search_distance, verbose):
        vectordbkwargs = {"search_distance": search_distance, "k": top_k, "search_type": search_type}
        
        qa = ConversationalRetrievalChain.from_llm(llm, db.as_retriever(search_kwargs=vectordbkwargs), chain_type=chain_type, memory=memory, verbose=verbose, return_source_documents=True, callbacks=[callback_handlers.DebugCallbackHandler()])

        return qa

    def _get_memory(self, llm, max_tokens):
        memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=max_tokens, memory_key="chat_history", return_messages=True, input_key="question", output_key="answer")    
        
        return memory
     
    def query(self, input):

        result = self.qa_chain({"question": input})

        source_docs = [{"document": os.path.basename(d.metadata['source']).split('.')[0], "page": d.metadata['page']} if 'page' in d.metadata else os.path.basename(d.metadata['source']).split('.')[0] for d in result["source_documents"]]

        ai_results = AIResult(result['answer'], source_docs) 

        return ai_results
    
