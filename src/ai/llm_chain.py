import os

from langchain import PromptTemplate
from langchain.chains import LLMChain as llm_chain
from langchain.memory import ConversationTokenBufferMemory

from shared.selector import get_embedding, get_llm
from documents.vector_database import get_database

from ai.llm_chain_configuration import LLMChainConfiguration
from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult


class LLMChain(AbstractAI):

    def configure(self, json_args) -> None:        
        self.configuration = LLMChainConfiguration(json_args)
        llm = get_llm(self.configuration.run_locally, float(self.configuration.ai_temp), -1)#self.configuration.max_tokens)
        
        self.chain = llm_chain(llm=llm, verbose=self.configuration.verbose, prompt=PromptTemplate.from_template("{query}"))
     
    def query(self, input):

        result = self.chain({"query": input})

        ai_results = AIResult(result['text']) 

        return ai_results
    
