
from simple_value_object import ValueObject, invariant
from ..genotype.operatord.selection import Selection
from ..genotype.operatord.crossover import Crossover
from ..genotype.operatord.mutation import Mutation


class OperatorList(ValueObject):

    def __init__(self, selection, crossover, mutation) -> None:
        pass

    @invariant
    def check_selection(cls, instance) -> bool:
        return isinstance(instance.selection, Selection)

    @invariant
    def check_crossover(cls, instance) -> bool:
        return isinstance(instance.crossover, Crossover)

    @invariant
    def check_mutation(cls, instance) -> bool:
        return instance.mutation is None or isinstance(instance.mutation, Mutation)

