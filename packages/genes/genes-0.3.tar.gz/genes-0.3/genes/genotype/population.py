
from .creature import Creature
from typing import List


class Population:

    _population: List[Creature]
    _iter_next: int = 0

    def __init__(self, population: List[Creature]):
        self._population = population

    def __getitem__(self, item: int) -> Creature:
        return self._population[item]

    def __iter__(self):
        self._iter_next = 0
        return self

    def __next__(self):
        if self._iter_next < len(self._population):
            result = self._population[self._iter_next]
            self._iter_next += 1
            return result
        else:
            raise StopIteration

    def size(self) -> int:
        return len(self._population)

    def add(self, creature: Creature) -> None:
        self._population.append(creature)

    def sort_by_fitness(self) -> None:
        self._population.sort(key=lambda item: item._fitness, reverse=True)

    def __str__(self):
        result = []
        for i in self._population:
            result.append('\t'.join((i.fitness().__str__(), i.genotype().__str__())))
        return '\n'.join(result)
