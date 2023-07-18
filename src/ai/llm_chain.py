import os

from langchain import PromptTemplate
from langchain.chains import LLMChain as llm_chain
from langchain.memory import ConversationTokenBufferMemory

from shared.selector import get_llm, get_chat_model

from ai.configurations.llm_chain_configuration import LLMChainConfiguration
from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult


class LLMChain(AbstractAI):

    def configure(self, json_args) -> None:        
        self.configuration = LLMChainConfiguration(json_args)
        if self.configuration.chat_model:
            llm = get_chat_model(self.configuration.run_locally, float(self.configuration.ai_temp))
        else:
            llm = get_llm(self.configuration.run_locally, float(self.configuration.ai_temp), -1)#self.configuration.max_tokens)

        memory = self._get_memory(llm, self.configuration.max_tokens) if self.configuration.use_memory else None                
        
        if self.configuration.prompt:
            if "inputs" in self.configuration.prompt:
                prompt = PromptTemplate.from_template(self.configuration.prompt)
            else:
                raise Exception("Prompt must contain 'inputs' key")
        else:
            prompt = PromptTemplate.from_template("{inputs}")

        self.chain = llm_chain(llm=llm, memory=memory, verbose=self.configuration.verbose, prompt=prompt)

    def _get_memory(self, llm, max_tokens):
        memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=max_tokens, memory_key="chat_history", return_messages=True, input_key="question", output_key="answer")    
        
        return memory
     
    def query(self, input):

        result = self.chain(inputs=input)
        
        ai_results = AIResult(result, result['text']) 

        return ai_results
    