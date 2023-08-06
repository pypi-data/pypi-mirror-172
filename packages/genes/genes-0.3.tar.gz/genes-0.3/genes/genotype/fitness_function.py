
from abc import ABC
from abc import abstractmethod
from .genotype import Genotype


class FitnessFunction(ABC):

    @abstractmethod
    def fit(self, genotype: Genotype) -> float:
        pass
