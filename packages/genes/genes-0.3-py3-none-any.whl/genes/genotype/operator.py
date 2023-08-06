
from abc import ABC, abstractmethod
from .population import Population


class Operator(ABC):

    @abstractmethod
    def do(self, population: Population) -> Population:
        pass

    def get_stats(self) -> dict:
        pass
