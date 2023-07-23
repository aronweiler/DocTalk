from abc import ABC, abstractmethod
from ai.ai_result import AIResult
from ai.agent_tools.utilities.registered_settings import RegisteredSettings


class AbstractAI(ABC):
    @abstractmethod
    def query(self, input) -> AIResult:
        pass

    @abstractmethod
    def configure(self, registered_settings: RegisteredSettings, json_args) -> None:
        pass
