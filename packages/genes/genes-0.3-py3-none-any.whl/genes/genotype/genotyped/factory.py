from ..genotype import Genotype
from .error.genotype_factory_error import GenotypeFactoryError


CHAR_0 = '0'
CHAR_1 = '1'


class Factory:

    @staticmethod
    def create_from_string(input: str) -> Genotype:
        genotype = []
        for char in input:
            if char == CHAR_0:
                genotype.append(False)
            elif char == CHAR_1:
                genotype.append(True)
            else:
                raise GenotypeFactoryError(char)
        return Genotype(genotype)
