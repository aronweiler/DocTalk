from abc import ABC, abstractmethod


class AbstractTool(ABC):
    @abstractmethod
    def run(self, query) -> str:
        pass

    @abstractmethod
    def configure(
        self,
        memory=None,
        override_llm=None,
        json_args=None,
    ) -> None:
        pass
