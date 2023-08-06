"""
Genes

Simple library for playing with genetic algorithms

Documentation: https://github.com/lbacik/genes

"""

from .genotype.genotype import Genotype
from .genotype.population import Population
from .genotype.fitness_function import FitnessFunction
from .genotype.populationd import factory as population_factory
from .genalg.factoryd.params import GAFactoryParams
from .genalg.factory import create_from_operator_params as genes_api_from_params_factory
