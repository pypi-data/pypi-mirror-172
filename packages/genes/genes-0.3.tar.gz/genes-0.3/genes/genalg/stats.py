from abc import ABC, abstractmethod

from ..genotype.population import Population


class Stats(ABC):

    FIT_MIN = 'min'
    FIT_MAX = 'max'
    FIT_AVR = 'avr'
    POPULATION_INDIVIDUALS = 'individuals'

    @abstractmethod
    def add_fit_stats(self, population: Population) -> None:
        pass

    @abstractmethod
    def add_action_stats(self, stats: dict) -> None:
        pass
