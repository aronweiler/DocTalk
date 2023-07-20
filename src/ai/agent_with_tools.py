from shared.selector import get_llm, get_chat_model
from langchain.memory import ConversationTokenBufferMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType

import re
import json

from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult

from ai.configurations.react_agent_configuration import AgentWithToolsConfiguration

from ai.agent_tools.utilities.tool_loader import load_tools

class AgentWithTools(AbstractAI):

    def configure(self, json_args) -> None:        
        self.configuration = AgentWithToolsConfiguration(json_args)

        if self.configuration.chat_model:
            router_llm = get_chat_model(self.configuration.run_locally, ai_temp=float(self.configuration.ai_temp))    
            agent_type = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION
        else:
            router_llm = get_llm(self.configuration.run_locally, ai_temp=float(self.configuration.ai_temp))
            agent_type = AgentType.CONVERSATIONAL_REACT_DESCRIPTION

        memory = self._get_memory(router_llm) if self.configuration.use_memory else None

        tools = load_tools(json_args, memory, None)

        self.agent_chain = initialize_agent(tools, router_llm, agent=agent_type, verbose=True, memory=memory, handle_parsing_errors=self._handle_error, agent_kwargs={"system_message": self.configuration.system_message})     


    def _get_memory(self, llm):
        memory = ConversationTokenBufferMemory(llm=llm, memory_key="chat_history", return_messages=True)    
        
        return memory
    

    def query(self, input):

        result = self.agent_chain.run(input=input)

        ai_results = AIResult(result, result) 

        return ai_results    
    

    # def extract_json_from_string(self, input_string:str):
    #     # Regular expression to find a JSON object within the string
    #     json_pattern = r'\{(?:[^{}]|(\?R))*\}'

    #     # Search for the JSON pattern in the input string
    #     json_matches = re.findall(json_pattern, input_string.replace('\n', ''))

    #     # Check if there are any JSON objects found
    #     if json_matches:
    #         # Parse the first JSON object found (you can modify this logic based on your requirements)
    #         first_json_string = json_matches[0]
    #         try:
    #             json_data = json.loads(first_json_string)
    #             return json_data
    #         except json.JSONDecodeError as e:
    #             print("Error parsing JSON:", str(e))
    #     else:
    #         print("No JSON object found in the input string.")
    #         return None

    def _handle_error(self, error) -> str:
        # json_data = self.extract_json_from_string(error.args[0])
        # if json_data:
        #     return json_data
        # else:
        return "extract and return"