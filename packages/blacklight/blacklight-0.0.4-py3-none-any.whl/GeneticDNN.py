'''
Genetic Deep Neural Net Topology Optimization
=================================
@author: Cole Agard
The goal is to use Genetic Algorithms to explore and create new
topologies for Deep Neural Nets. Fitness function is Accuracy,
and the GENES used are the individual topologies.

Hypothesis:
DNN topologies will converge to either a local maximum or an
absolute maximum over the evolution process, offering better
performance than a DNN with randomly selected topology. For this first
experiment, I will use equivalent activation functions (ReLu) and SGD for
Back-propogation, holding everything EXCEPT the topology constant.

Tools:
Might need to convert code to Rust or C++ to improve speed, python is
a proof of concept that will run INCREDIBLY slowly. I assume I will be
limited to only a few generations with only 10 or so samples.

notes from Wednesday.
1) in each generation, assign male and female and random inidividuals. make there more males than females
and then allow each male to breed in proportion to its performance in a given round.

2)dont train each network for the same number of epochs. Use monte carlo to determine how to much time to invest in each
individual. then you can set it to go for x minutes, instead of teaining each one for x epochs

3)we need to do a literature review.

4)every ten rounds throw in a new set of data points. These should maybe be from the set that the agorithm hasn't see before. Focus
the culling algorithm on hiw each individual does on this new dataset. this would represent an earthquake maybe, or something the population








'''

import random
import statistics

import tensorflow as tf
from tensorflow import keras

from src.Dataset import *
from joblib import Parallel, delayed
import multiprocessing

# Can also be set using the AUTOGRAPH_VERBOSITY environment variable
tf.autograph.set_verbosity(0)


# Verbosity is now 0
class individual:
    """
    An individual is a KERAS model.
    Genes are the array dimensions, passed: [4, 5, 6]  would be a model consisting of
    an input layer, a layer of 4 dense nodes, a layer of 5 dense nodes, a layer of 6 dense
    nodes, and an output layer.
    """
    fitness = 0
    chromosomeone = []

    def __init__(self, parentOne=None, parentTwo=None, population=None):
        """
        Initializes model dimensions with random size if chromosomeFromParentOne = None, otherwise initialize
        with input array to describe shape.

        TODO:
            Chromasome -> dictionary with number of nodes per layer in key, type of node in value.

        """
        self.population = population if population is not None else "WHOA THERE BUDDY THIS INDIVIDUAL NEEDS ITS CLAN"
        self.fitness = 0
        self.chromosomeone = None
        self.chromosometwo = None
        if parentOne == None and parentTwo == None:
            self.chromosomeone = {}
            initiallen = random.randint(1, 13)
            for elem in range(initiallen):
                # {random int between 0 and 64: Type = ReLu} -> Eventually we want to make this select between Relu, Conv2D, and other node types.
                self.chromosomeone[random.randint(0, 64)] = 'relu'

            self.chromosometwo = {}
            initiallen = random.randint(1, 13)
            for elem in range(initiallen):
                # {random int between 0 and 64: Type = ReLu} -> Eventually we want to make this select between Relu, Conv2D, and other node types.
                self.chromosometwo[random.randint(0, 64)] = 'relu'
        else:
            self.chromosomeone = parentOne.chromosomeone
            self.chromosometwo = parentTwo.chromosomeone
            # Crossover, using parent 1's chromosome and parent 2's chromosome
            self.crossover()
            # Mutate some
            self.mutation()

        self.train_features, self.train_labels, self.test_features, self.test_labels, self.val_features, self.val_labels = self.population.goal.grabneuralnetdata()
        self.model = self.make_model(output_bias=None, layerdef=self.chromosomeone, train_features=self.train_features)

    def make_model(self, output_bias=None, layerdef=None, train_features=None):
        """
        Creates keras dense model by using the layerdefinition array passed. The Metrics for training are defined
        here as well, Including AUC, Precision, Recall, and Accuracy. The model is returned.
        :param output_bias:
        :param layerdef:
        :param train_features:
        :return:
        """
        if output_bias is not None:
            output_bias = tf.keras.initializers.Constant(output_bias)
        if layerdef is None:
            print("There were no charactaristics passed to generate individual model.")
            return None
        else:
            layerlist = [tf.keras.layers.Dense(train_features.shape[-1], activation='relu', input_shape=(train_features.shape[-1],))] + [
                tf.keras.layers.Dense(i, activation=layerdef.get(i)) for i in layerdef.keys()] + [
                            keras.layers.Dense(1, activation='sigmoid')]
            model = keras.Sequential(layerlist)
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                loss=keras.losses.BinaryCrossentropy(),
                metrics=[
                    keras.metrics.TruePositives(name='tp'),
                    keras.metrics.FalsePositives(name='fp'),
                    keras.metrics.TrueNegatives(name='tn'),
                    keras.metrics.FalseNegatives(name='fn'),
                    keras.metrics.CategoricalAccuracy(name='accuracy'),
                    keras.metrics.Precision(name='precision'),
                    keras.metrics.Recall(name='recall'),
                    keras.metrics.AUC(name='auc'),
                ])
            return model

    def crossover(self):
        """
        Take half of the genes from the first parent, and the second half from the other parent. Splice them together,
        and add the offspring with this chromosomeFromParentOne to the offspring_crossover instance variable of a population. Then, add
        The offspring to the self.individuallist (population).

        ########################################################
         Chromasome 1   |     Chromasome 2   |     Chromasome 3
        ########################################################
        {12: 'softmax', |     {8: 'relu',    |    {8: 'relu',
         4: 'softmax',  |      2: 'relu',    |     2: 'relu',
         7: 'relu',     |      4: 'relu'}    |     4: 'softmax'}
         4: 'relu',     |      7: 'relu',    |
         7: 'Conv2D',   |      4: 'softmax'} |
         12: 'relu',    |                    |
         4: 'relu'}     |                    |
                        |                    |
         #######################################################
         #
         #                        CROSS
         #                         OVER
         #                  Random Choice: element 3.
         #######################################################
         #         Recombinant 1    |        Recombinant 2
         #######################################################
                {8: 'relu',         |     {12: 'softmax',
                 2: 'relu',         |      4: 'softmax',
                 4: 'relu',         |      7: 'relu',
                 4: 'relu',         |      7: 'relu',
                 7: 'Conv2D'        |      4: 'softmax'}
                 12: 'relu'         |
                 4: 'relu'}         |

        TODO:
            Per INDIVIDUAL
                Chromasome -> 1
                Chromasome -> 2
                Chromasome -> 3
            P: We need to select one of the three Chromosomes gets RUN by the brain (population)
            A: in INDIVIDUAL
                    self.dominantChromisome = choice of the three carried
                    self.chromasomeList = [Chromasome 1, Chromasome 2, Chromasome 3]
                    Need to define:
                        List of predetermined structures that perform well for certain tasks:
                            EX, ConvDNET2D -> images (copy structure, compare similarity to all three chromasomes
                                Collapse dictionaries into a list, and compare to database of chromasomes
                    At end of simulation, add the best performer's chromosome to the dataset.
                        "Phenotype expression"
        :return:
        """

        crossover_point = np.uint8(np.random.randint(0, len(self.chromosomeone.keys())))
        # Recombinant one is the result of parental gene 1 + parental gene 2's crossover point
        recombinant_one = {}
        recombinant_two = {}
        base_for_recombinant_one = list(self.chromosomeone.keys())[0:crossover_point]
        link_for_recombinant_one = list(self.chromosometwo.keys())[(crossover_point % len(self.chromosometwo.keys())):]


        for key in base_for_recombinant_one:
            recombinant_one[key] = self.chromosomeone.get(key)
        # The recombinant will have  of its genes taken from the second parent.
        for key in link_for_recombinant_one:
            recombinant_one[key] = self.chromosometwo.get(key)

        # TODO: make it choose based on previous knowledge.

        # TODO: this needs some work, I think that one way to do this is to sample proportions between the two groups using numpy? ? ?
        recombinant_chance_1_list = list(('A',) * int((len(link_for_recombinant_one) / len(self.chromosomeone.keys())) * 100))
        recombinant_chance_2_list = list(('B',) * int((len(link_for_recombinant_one) / len(self.chromosomeone.keys())) * 100))
        parental_chance_1_list = list(('C',) * int((100 - ((len(link_for_recombinant_one) / len(self.chromosomeone.keys())) * 100) / 2)))
        parental_chance_2_list = list(('D',) * int((100 - ((len(link_for_recombinant_one) / len(self.chromosomeone.keys())) * 100) / 2)))

        genome_chances = recombinant_chance_1_list + recombinant_chance_2_list + parental_chance_1_list + parental_chance_2_list

        picked_genome = np.random.choice(genome_chances)

        if picked_genome == 'A':
            self.chromosomeone = recombinant_one

        elif picked_genome == 'B':
            self.chromosomeone = recombinant_two

        elif picked_genome == 'C':
            self.chromosomeone = self.chromosomeone

        elif picked_genome == 'D':
            self.chromosomeone = self.chromosometwo

    def mutation(self):
        """
        Mutates one random gene at random in the offspring pool. This value can be changed by increaseing the threshold for
        ifmutate.
        :return:
        """
        # Mutation changes a single gene in each offspring randomly.
        offspring_crossover = self.chromosomeone
        for idx in range(len(offspring_crossover)):
            # The random value to be added to the gene.
            random_value = random.randint(0, 4)
            ifmutate = random.random()
            if ifmutate < .2:
                index = random.randint(0, len(offspring_crossover) - 1)
                # TODO come back later to this, it works but not as you THINK
                offspring_crossover[list(offspring_crossover.keys())[idx] + random_value] = offspring_crossover[
                    list(offspring_crossover.keys())[idx]]
        self.chromosomeone = offspring_crossover

    def getfitness(self):
        """
        Trains the individual on the training data in population goal. Sets a instance variable fitness
        based on the auc metric after training. This also returns that value.
        TODO:
            This works, but we need to add epochs as an input param into thefunction.

        :return:
        """
        EPOCHS = 1000
        BATCH_SIZE = 2048

        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_auc',
            verbose=1,
            patience=10,
            mode='max',
            restore_best_weights=True)

        self.model.fit(self.train_features,
                       self.train_labels,
                       batch_size=BATCH_SIZE,
                       epochs=EPOCHS,
                       callbacks=[early_stopping],
                       validation_data=(self.val_features, self.val_labels), verbose=0)
        # trainresults = self.model.predict(train_features, batch_size=BATCH_SIZE, verbose=0)
        # testrestuls = self.model.predict(test_features, batch_size=BATCH_SIZE, verbose=0)
        results = self.model.evaluate(self.test_features, self.test_labels, batch_size=BATCH_SIZE, verbose=0)
        fitness = results[-1]  # the auc value for this run is used as a metric.
        self.fitness = fitness
        return fitness


class population:
    """
    A population of DNN topologies that can be evaluated. Their GOAL is the current dataset that this population wants to work on.
    """

    def __init__(self, numberofindividuals, numparents, inputfilelocation):
        """
        Initialize a population of (numberofindividuals) individuals, and specify the number of
        parents allowed to breed at one time in this population. Individuals are initilized with random shape here.
        :param numberofindividuals:
        :param numparents:
        """
        self.goal = Dataset(inputfilelocation)
        self.goal.loaddeepneuralnetdata()
        self.numindividual = numberofindividuals
        self.individuallist = np.asarray([individual(population=self) for _ in range(self.numindividual)])
        self.num_parents_mating = numparents


    def findfitness(self, listofindividuals):
        """
        Return the fitness of all individuals in a population.
        :param listofindividuals:
        :return: list of floats, each float is # between 0 and 1,
        """
        fitness = [self.individuallist[i].getfitness() for i in range(len(self.individuallist))]
        return fitness

    def findparents(self):
        """
        Selecting the best individuals in the current generation as parents for producing the offspring of the next
        generation.
        """
        num_parents = self.num_parents_mating
        fitness = self.findfitness()
        parents = []
        for parent_num in range(num_parents):
            max_fitness_idx = np.where(fitness >= np.max(fitness))
            max_fitness_idx = max_fitness_idx[0][0]
            parents.append(self.individuallist[max_fitness_idx])
            fitness[max_fitness_idx] = -99999999999
        self.parents = parents
        individuals = self.individuallist
        for individual in range(len(self.individuallist)):
            if individuals[individual] not in parents:
                np.delete(individuals, individual)
        self.individuallist = individuals
        return parents

    # We want to ExPeRiMeNt WiTh DiFfErEnT TyPeS oF SeXy TiMe
    def reproduce(self):
        """
        Right now, pick two parents randomly from thdef is not Nonee population. Take their genomes and create a new individual.
        Add this individual to the individuallist.
        """
        parents = self.parents
        for _ in range(self.num_parents_mating):
            parents = np.random.choice(parents, 2, replace=False)
            newindividual = individual(parents[0], parents[1], population=self)
            np.append(self.individuallist, newindividual)


class environment:
    """ An environment to hold our population(s) of individuals, run them, and return results. """
    def __init__(self, numpopulations, individualsperpopulation, numberofparentsmating, numberofgenerations, environmentgoal):
        self.numpop = numpopulations
        self.indperpop = individualsperpopulation
        self.numparents = numberofparentsmating
        self.numgen = numberofgenerations
        self.environmentgoal = environmentgoal
        self.populationlist = []

        for _ in range(numpopulations):
            self.populationlist.append(population(self.indperpop, self.numparents, self.environmentgoal))

    def runonepopulation(self, index):
        population = self.populationlist[index]
        for generation in range(self.numgen):
            print("Generation : ", generation)
            print("Number of individuals : ", len(population.individuallist))
            population.findparents()
            population.reproduce()
        return max([population.individuallist[i].fitness for i in range(len(population.individuallist))])

    def runenvironment(self):
        """
        This is highly experimental and may not work, basically splits each population onto a different CPU thread and then the
        runs them in parallel.
        """
        num_cores = multiprocessing.cpu_count()
        best_of_the_populations = Parallel(n_jobs=num_cores)(delayed(environment.runonepopulation(self, i) for i in range(len(self.numpopulations))))
