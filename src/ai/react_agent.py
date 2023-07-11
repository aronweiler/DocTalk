from shared.selector import get_llm
from langchain.memory import ConversationTokenBufferMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult

from ai.react_agent_configuration import ReActAgentConfiguration

from ai.agent_tools.utilities.tool_loader import load_tools

class ReActAgent(AbstractAI):

    def configure(self, json_args) -> None:        
        self.configuration = ReActAgentConfiguration(json_args)

        router_llm = get_llm(self.configuration.run_locally, float(self.configuration.ai_temp))
        memory = self._get_memory(router_llm, self.configuration.max_tokens) if self.configuration.use_memory else None        

        tools = load_tools(json_args, memory, None)

        self.agent_chain = initialize_agent(tools, router_llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)     


    def _get_memory(self, llm, max_tokens):
        memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=max_tokens, memory_key="chat_history", return_messages=True)    
        
        return memory
    

    def query(self, input):

        result = self.agent_chain.run(input=input)

        ai_results = AIResult(result) 

        return ai_results

