
from .genotype import Genotype


class Creature:

    def __init__(self, genotype: Genotype, fitness: float = 0):
        self._genotype = genotype
        self._fitness = fitness

    def __getitem__(self, item):
        return self._genotype[item]

    def genotype(self) -> Genotype:
        return self._genotype

    def fitness(self) -> float:
        return self._fitness

    def set_fitness(self, value: float) -> None:
        self._fitness = value
