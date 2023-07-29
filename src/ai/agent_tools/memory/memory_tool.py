import logging
import json

from ai.agent_tools.utilities.abstract_tool import AbstractTool
from ai.agent_tools.memory.memory_tool_configuration import MemoryToolConfiguration
from ai.agent_tools.memory.memory_action import MemoryAction, MemoryActionType
from memory.long_term.database.memories import Memories, Memory
from memory.long_term.database.users import Users, User


class MemoryTool(AbstractTool):
    def configure(
        self, memory=None, override_llm=None, json_args=None
    ) -> None:
        self.configuration = MemoryToolConfiguration(json_args)
        self.memories = Memories(self.configuration.db_env_location)
        self.users = Users(self.configuration.db_env_location)

    def run(self, query: str) -> str:
        logging.debug("MemoryTool got query: " + query)

        try:
            json_args = json.loads(query)

            memory_action = MemoryAction.from_json(json_args)

            with self.users.session_context(self.users.Session()) as session:
                if memory_action.memory_action == MemoryActionType.add_memory:
                    self.memories.store_text_memory(session,
                        memory_text=memory_action.text,
                        associated_user_email=memory_action.associated_user_email,
                        interaction_id=memory_action.interaction_id,
                    )
                    return "Memory successfully stored!"
                elif memory_action.memory_action == MemoryActionType.search_memory:
                    memories = self.memories.find_memories(session,
                        memory_text_search_query=memory_action.text,
                        associated_user_email=memory_action.associated_user_email,
                        interaction_id=memory_action.interaction_id,
                        eager_load=[Memory.user],
                        search_type=memory_action.search_type,
                        top_k=self.configuration.top_k
                    )

                    memories_output = []
                    for memory in memories:
                        memory_string = f"{memory.record_created}:"
                        if memory.user is not None:
                            memory_string += f" associated_user: {memory.user.name} ({memory.user.email})"

                        if memory.interaction_id is not None:
                            memory_string += (
                                f" interaction_id: '{memory.interaction_id}'"
                            )

                        memory_string += f" memory: '{memory.memory_text}'"
                        memories_output.append(memory_string)

                    if len(memories_output) > 0:
                        return "Found memories: " + "\n".join(memories_output)
                    else:
                        return "No memories found related to that query.  You should query the user for more information."
                else:
                    return "No memories found related to that query."
        except:
            return """Fail!  Check your input and try again."""


    

