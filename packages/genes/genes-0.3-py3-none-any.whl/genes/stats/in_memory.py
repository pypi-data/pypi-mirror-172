from .. import Population
from ..genalg.stats import Stats


class InMemoryStats(Stats):

    def __init__(self, record_genotypes=False):
        self.record_genotypes = record_genotypes
        self.population_history = []
        self.population_history_stats = []

    def add_fit_stats(self, population: Population) -> None:
        self.collect_population_stats(population)
        if self.record_genotypes:
            self.population_history.append(population)

    def add_action_stats(self, stats: dict) -> None:
        pass

    def collect_population_stats(self, population: Population) -> None:
        record = {}
        fit_min = fit_max = None
        hashes = set()
        fit_sum = 0
        for c in population:
            if fit_min is None or c.fitness() < fit_min:
                fit_min = c.fitness()
            if fit_max is None or c.fitness() > fit_max:
                fit_max = c.fitness()
            fit_sum += c.fitness()
            hashes.add(hash(c.genotype().__str__()))

        record[self.FIT_MIN] = fit_min
        record[self.FIT_MAX] = fit_max
        record[self.FIT_AVR] = fit_sum / population.size()
        record[self.POPULATION_INDIVIDUALS] = len(hashes)

        self.population_history_stats.append(record)
