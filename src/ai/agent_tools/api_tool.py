import logging

from shared.selector import get_llm

from ai.configurations.api_tool_configuration import APIToolConfiguration
from ai.agent_tools.utilities.abstract_tool import AbstractTool

class APITool(AbstractTool):
    def configure(
        self, registered_settings, memory=None, override_llm=None, json_args=None
    ) -> None:
        self.configuration = APIToolConfiguration(json_args=json_args)
        # Configure the local Gorilla LLM 
        self.api_llm = get_llm(local=self.configuration.run_locally, local_model_path=self.configuration.api_llm_model, ai_temp=self.configuration.ai_temp)

    def run(self, query: str) -> str:
        logging.debug("API Tool got query: " + query)
        
        result = self.api_llm.predict(self.configuration.api_llm_prompt.format(query=query))
        
        return result
