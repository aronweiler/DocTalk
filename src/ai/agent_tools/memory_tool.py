import logging
import json
from dotenv import load_dotenv

from ai.agent_tools.utilities.abstract_tool import AbstractTool
from ai.configurations.memory_tool_configuration import MemoryToolConfiguration
from memory.long_term.database.memories import Memories, Memory
from memory.long_term.database.users import Users, User
from memory.long_term.database.vector_database import SearchType


class MemoryTool(AbstractTool):
    def configure(
        self, registered_settings, memory=None, override_llm=None, json_args=None
    ) -> None:
        self.configuration = MemoryToolConfiguration(json_args)
        self.memories = Memories(self.configuration.db_env_location)
        self.users = Users(self.configuration.db_env_location)

    def run(self, query: str) -> str:
        logging.debug("MemoryTool got query: " + query)

        try:
            json_args = json.loads(query)

            with self.users.session_context(self.users.Session()) as session:
                # Is there a user associated with this memory?
                user = None
                if "associated_user" in json_args:
                    user = self.users.find_user_by_email(session,
                        email=json_args["associated_user"], eager_load=[]
                    )

                # Is there an interaction id associated with this memory?
                interaction_id = None
                if "interaction_id" in json_args:
                    interaction_id = json_args["interaction_id"]

                if json_args["action"] == "add_memory":
                    self.memories.store_text_memory(session,
                        memory_text=json_args["memory"],
                        associated_user=user,
                        interaction_id=interaction_id,
                    )
                    return "Memory successfully stored!"
                elif json_args["action"] == "search_memory":
                    # Search for a memory
                    try:
                        search_type = SearchType[json_args["search_type"]]
                    except:
                        # dumb
                        search_type = SearchType.SIMILARITY

                    memories = self.memories.find_memories(session,
                        memory_text_search_query=json_args["query"],
                        associated_user=user,
                        interaction_id=interaction_id,
                        eager_load=[],
                        search_type=search_type,
                        top_k=self.configuration.top_k
                    )

                    memories_output = []
                    for memory in memories:
                        # set moniker to "Conversation" if it's not a memory, otherwise set it to "Memory"
                        memory_string = f"{memory.record_created}:"
                        if memory.user is not None:
                            memory_string += f" associated_user: '{memory.user.name}'"

                        if memory.interaction_id is not None:
                            memory_string += (
                                f" interaction_id: '{memory.user.interaction_id}'"
                            )

                        memory_string += f" memory: '{memory.memory_text}'"
                        memories_output.append(memory)

                    if len(memories_output) > 0:
                        return "Found memories: " + "\n".join(memories_output)
                    else:
                        return "No memories found related to that query.  You should query the user for more information."
                else:
                    return "No memories found related to that query."
        except:
            return """Fail!  Probably badly formed input.  
Input to this tool should be a SINGLE JSON string, with an action of 'add_memory' or 'search_memory'.  
e.g. when adding memory: 
'{{'action': \"add_memory\", \"associated_user\": \"John\", \"interaction_id\": \"12345-1234-xyz\", \"memory\": \"the user likes ice cream\"}}', 
or '{{'action': \"add_memory\", \"memory\": \"The weather tool failed to respond\"}}'. 

e.g. when searching memory, search_type should be either 'SIMILARITY' or 'KEY_WORD': 
'{{\"action\": \"search_memory\", \"associated_user\": \"John\", \"query\": \"users favorite food\", \"search_type\": \"KEY_WORD\"}}', 
or '{{'action': \"search_memory\", \"query\": \"recent failed tools\", \"search_type\": \"SIMILARITY\"}}'. 

Remember, the input must be a SINGLE JSON string."""
