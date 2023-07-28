from enum import Enum
from memory.long_term.database.vector_database import SearchType

class MemoryActionType(Enum):
    add_memory = "add_memory"
    search_memory = "search_memory"

class MemoryAction:
    def __init__(self, action: str, text: str, associated_user_email=None, interaction_id=None, search_type=None):
        
        if action is None:
            raise ValueError(f"memory_action must be either '{MemoryActionType.add_memory}', or '{MemoryActionType.search_memory}'.")

        if text is None:
            raise ValueError("'text' is a required field")
        
        self.text = text

        try:
            self.memory_action = MemoryActionType[action]
        except:
            raise ValueError(f"memory_action is not valid. memory_action must be either '{MemoryActionType.add_memory}', or '{MemoryActionType.search_memory}'.")

        
        self.associated_user_email = associated_user_email
        self.interaction_id = interaction_id

        try:
            if self.memory_action == MemoryActionType.search_memory:
                if search_type is None:
                    self.search_type = SearchType.similarity
                else:
                    self.search_type = SearchType[search_type.lower()]
        except:
            raise ValueError(f"search_type {search_type} is not valid. search_type must be either '{SearchType.key_word}', or '{SearchType.similarity}'.")

    # Static method to construct the class from a json object
    @staticmethod
    def from_json(json_args):
        return MemoryAction(
            action=json_args["memory_action"],
            text=json_args["text"],
            associated_user_email=json_args["associated_user"] if "associated_user" in json_args else None,
            interaction_id=json_args["interaction_id"] if "interaction_id" in json_args else None,
            search_type=json_args["search_type"] if "search_type" in json_args else None,
        )
    