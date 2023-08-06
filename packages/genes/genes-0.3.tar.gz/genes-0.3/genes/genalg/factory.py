from .api import GeneticAlgorithmApi
from .config import Config
from .factoryd.params import GAFactoryParams
from .operator_list import OperatorList
from ..genotype.fitness_function import FitnessFunction
from ..genotype.operatord.crossover import Crossover
from ..genotype.operatord.mutation import Mutation
from ..genotype.operatord.selection import Selection
from ..stats.in_memory import InMemoryStats


def create_from_operator_list(fitness_function: FitnessFunction, operators: OperatorList) -> GeneticAlgorithmApi:
    actions = [
        operators.selection,
        operators.crossover,
    ]
    if operators.mutation is not None:
        actions.append(operators.mutation)

    return GeneticAlgorithmApi(None, Config(), fitness_function, actions, InMemoryStats())


def create_from_operator_params(fitness_function: FitnessFunction, params: GAFactoryParams) -> GeneticAlgorithmApi:

    selection = Selection({
        Selection.CREATURES_TO_CHOOSE: params.population
    })

    crossover = Crossover({
        Crossover.CHILDREN_PER_PARENTS: params.children_per_pair,
        Crossover.POPULATION_SIZE: params.population,
        Crossover.CROSSOVER_TYPE: params.crossover_type,
    })

    if params.mutation_probability is not None:
        mutation = Mutation({
            Mutation.MUTATION_PROBABILITY: params.mutation_probability,
        })
    else:
        mutation = None

    return create_from_operator_list(fitness_function, OperatorList(selection, crossover, mutation))


# def create_params() -> GAFactoryParams:
#     return GAFactoryParams()