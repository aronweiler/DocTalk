from abc import ABC, abstractmethod
from ai.abstract_ai import AbstractAI
from pydantic import BaseModel

class Runner(ABC):

    @abstractmethod
    def run(self, abstract_ai: AbstractAI):
        pass
