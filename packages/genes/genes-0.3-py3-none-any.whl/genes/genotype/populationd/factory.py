from random import randint
from typing import List

from ..creature import Creature
from ..genotype import Genotype
from ..population import Population


def generate_genotype(length: int, percentage: int = 50) -> Genotype:
    genotype: List[bool] = []
    for i in range(1, length):
        genotype.append(True if randint(1, 101) <= percentage else False)
    return Genotype(genotype)


def create_population(number: int, length: int, percentage: int = 50) -> Population:
    population: Population = Population([])

    for i in range(0, number):
        genotype: Genotype = generate_genotype(length, percentage)
        population.add(Creature(genotype))

    return population
