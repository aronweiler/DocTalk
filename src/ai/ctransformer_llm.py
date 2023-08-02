import logging

from ctransformers import AutoModelForCausalLM

from shared.selector import get_llm, get_chat_model
from utilities.token_helper import num_tokens_from_string

from ai.configurations.llm_chain_configuration import LLMChainConfiguration
from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult


class CTransformersLLM(AbstractAI):
    def configure(self, json_args) -> None:
        self.configuration = LLMChainConfiguration(json_args)        
        
        self.llm = AutoModelForCausalLM.from_pretrained(self.configuration.model, model_type="starcoder", max_new_tokens=1000, gpu_layers=50)   

    def query(self, input):      

        result = self.llm(input)

        ai_results = AIResult(result, result)

        return ai_results