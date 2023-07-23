from abc import ABC, abstractmethod
from ai.agent_tools.utilities.registered_settings import RegisteredSettings

class AbstractTool(ABC):

    @abstractmethod
    def run(self, query) -> str:
        pass

    @abstractmethod
    def configure(self, registered_settings:RegisteredSettings, memory = None, override_llm = None, json_args = None) -> None:
        pass