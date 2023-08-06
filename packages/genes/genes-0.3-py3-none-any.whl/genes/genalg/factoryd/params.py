
from simple_value_object import ValueObject

from ...genotype.operatord.crossover import Crossover


class GAFactoryParams(ValueObject):
    def __init__(self,
                 population,
                 selection_limit,
                 children_per_pair=4,
                 crossover_type=Crossover.CROSSOVER_TYPE_MONO,
                 mutation_probability=None,
                 ):
        pass
