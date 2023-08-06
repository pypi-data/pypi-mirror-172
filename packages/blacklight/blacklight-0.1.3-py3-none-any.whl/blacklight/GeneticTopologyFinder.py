from GDNN import population


class GeneticTopologyFinder:
    """
    A general purpose runner for Blacklights neural network topology search
    """

    def __init__(self,
                 numpopulations=5,
                 individualsperpopulation=5,
                 numberofparentsmating=2,
                 numberofgenerations=5):
        self.dataset = None
        self.num_pop = numpopulations
        self.ind_per_pop = individualsperpopulation
        self.num_parents_mating = numberofparentsmating
        self.num_generations = numberofgenerations
        self.model = None

    def fit(self, dataset):
        self.dataset = dataset
        this_population = population(self.ind_per_pop, self.num_parents_mating, self.dataset)
        for generation in range(self.num_generations):
            print("Generation : ", generation)
            print("Number of individuals : ", len(this_population.individuallist))
            this_population.findparents()
            this_population.reproduce()
        best_model = max([this_population.individuallist[i] for i in range(len(this_population.individuallist))],
                         key=lambda x: x.fitness)
        self.model = best_model.model

    def describe(self):
        self.model.describe()
