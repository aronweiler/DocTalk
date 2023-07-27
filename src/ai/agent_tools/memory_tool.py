import logging
import json
from dotenv import load_dotenv

from ai.agent_tools.utilities.abstract_tool import AbstractTool
from ai.configurations.memory_tool_configuration import MemoryToolConfiguration
from memory.long_term.vector_database import VectorDatabase

class MemoryTool(AbstractTool):
    def configure(
        self, registered_settings, memory=None, override_llm=None, json_args=None
    ) -> None:
        self.configuration = MemoryToolConfiguration(json_args)
        self.db = VectorDatabase(self.configuration.db_env_location)

    def run(self, query: str) -> str:
        # Expecting a JSON string
        # Example: 
        # {"action": "add_conversation", "user_info": {"user_name": "John", "user_age": 30, "user_location": "New York"}, "message": "Hello, how are you?"}
        # {"action": "search_conversation_memory", "user": "John", "query": "Asking how I am", "top_k": 5}        
        logging.debug("MemoryTool got query: " + query)

        try:
            json_args = json.loads(query)
                            
            with self.db.session_context(self.db.Session()) as s:
                if json_args["action"] == "add_conversation":
                    self.db.add_conversation(session=s, user_info=json_args["user_info"], message=json_args["message"], is_memory=True)
                    return "Memory successfully stored, no need to verify, or even alert the user!"
                elif json_args["action"] == "search_conversation_memory":
                    if "query" in json_args:
                        conversations = self.db.search_conversation_memory(session=s, query=json_args["query"], top_k=self.configuration.top_k)
                    elif "user" in json_args:
                        conversations = self.db.search_conversation_memory(session=s, query=json_args["query"], top_k=self.configuration.top_k)
                    else:
                        return "No query or user specified.  Please specify one or the other."
                    memories = []
                    for conversation in conversations:
                        # set moniker to "Conversation" if it's not a memory, otherwise set it to "Memory"
                        moniker = "Memory" if conversation.is_memory else "Conversation History"
                        memory = f"{moniker}: {conversation.record_created}, created by: {conversation.user.name if conversation.user else 'Unknown'}, message: {conversation.message}, additional_metadata: {conversation.additional_metadata}"
                        memories.append(memory)
        
                    return "Found memories: " + "\n".join(memories)
                else:
                    return "No memories found related to that query."
        except:
            return """Fail!  Probably badly formed input.  
Input should be a single JSON string. 
For example: 
{\"action\": \"add_conversation\", \"user_info\": {\"user_name\": \"John\", \"user_age\": 30, \"user_location\": \"New York\"}, \"message\": \"Hello, how are you?\"}
or
{\"action\": \"search_conversation_memory\", \"user\": \"John\", \"query\": \"Asking how I am\"}"""