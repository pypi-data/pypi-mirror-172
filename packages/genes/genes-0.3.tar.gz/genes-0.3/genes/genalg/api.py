
from typing import List, Optional
from logging import Logger
from .config import Config
from ..genotype.operator import Operator
from ..genotype.population import Population
from ..genotype.fitness_function import FitnessFunction
from .stats import Stats


class GeneticAlgorithmApi():

    def __init__(self,
                 logger: Optional[Logger],
                 config: Config,
                 fitness_function: FitnessFunction,
                 actions: List[Operator],
                 stats: Optional[Stats] = None
                 ) -> None:
        self._logger = logger
        self._config = config
        self._fitness_function = fitness_function
        self._actions: List[Operator] = actions
        self._population: Population = Population([])
        self.stats: Optional[Stats] = stats

    def init_population(self, population: Population) -> None:
        self._population = population
        self._fit_population()

    def population(self) -> Population:
        return self._population

    def next_generation(self) -> Population:
        if self._population is None:
            raise Exception('Population not initialized!')

        self._execute_actions()
        self._fit_population()
        return self._population

    def calculate(self, init_population: Population, generations: int) -> Population:
        self.init_population(init_population)
        last: Population = self._population
        for _ in range(0, generations):
            last =  self.next_generation()
        return last

    def _fit_population(self) -> None:
        for creature in self._population._population:
            creature._fitness = self._fitness_function.fit(creature.genotype())
        if self.stats:
            self.stats.add_fit_stats(self._population)

    def _execute_actions(self) -> None:
        generation: Population = self._population
        for action in self._actions:
            generation = action.do(generation)
            if self.stats:
                self.stats.add_action_stats(action.get_stats())

        self._population = generation

