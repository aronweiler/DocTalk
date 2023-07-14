import os
from utilities.callback_handlers import DebugCallbackHandler

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationTokenBufferMemory

from shared.selector import get_embedding, get_chat_model
from documents.vector_database import get_database

from ai.qa_chain_configuration import QAChainConfiguration
from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult

class QAChainAI(AbstractAI):

    def configure(self, json_args) -> None:        
        self.configuration = QAChainConfiguration(json_args)
        embeddings = get_embedding(self.configuration.run_locally)    
        db = get_database(embeddings, self.configuration.database_name) 
        llm = get_chat_model(self.configuration.run_locally, float(self.configuration.ai_temp))
        
        memory = self._get_memory(llm, self.configuration.max_tokens) if self.configuration.use_memory else None    
        
        self.qa_chain = self._get_chain(llm, memory, db, self.configuration.top_k, self.configuration.chain_type, self.configuration.search_type, self.configuration.search_distance, self.configuration.verbose)


    def _get_chain(self, llm, memory, db, top_k, chain_type, search_type, search_distance, verbose):
        vectordbkwargs = {"search_distance": search_distance, "k": top_k, "search_type": search_type}
        
        qa = ConversationalRetrievalChain.from_llm(llm, db.as_retriever(search_kwargs=vectordbkwargs), chain_type=chain_type, memory=memory, verbose=verbose, return_source_documents=True, callbacks=[DebugCallbackHandler()])

        return qa

    def _get_memory(self, llm, max_tokens):
        memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=max_tokens, memory_key="chat_history", return_messages=True, input_key="question", output_key="answer")    
        
        return memory
     
    def query(self, input):

        # If there is no memory, we have to fake it for the prompt.  
        # Langchain should be better about this and automatically hand it
        if self.configuration.use_memory:
            result = self.qa_chain({"question": input})
        else:
            result = self.qa_chain({"question": input, "chat_history": []})

        source_docs = [{"document": os.path.basename(d.metadata['source']).split('.')[0], "page": d.metadata['page']} if 'page' in d.metadata else os.path.basename(d.metadata['source']).split('.')[0] for d in result["source_documents"]]

        ai_results = AIResult(result, result['answer'], source_docs) 

        return ai_results
    
