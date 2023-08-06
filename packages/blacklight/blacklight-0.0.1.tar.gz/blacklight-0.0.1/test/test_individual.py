import unittest
from src.GeneticDNN import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class TestIndividual(unittest.TestCase):
    def test_initialization(self):
        thispopulation = population(3, 2, "Data/digit-recognizer/train.csv")
        individualone = individual(population=thispopulation)
        individualtwo = individual(population=thispopulation)
        individualonechromosomeone = individualone.chromosomeone
        for link in individualonechromosomeone.keys():
            base_pair = individualonechromosomeone.get(link)
            self.assertLess(int(link), 64)
            self.assertEqual(base_pair, 'relu')

        self.assertLess(len(individualonechromosomeone), 14)

    def test_each_individuals_data(self):
        thispopulation = population(20, 3, "Data/digit-recognizer/train.csv")
        data = Dataset('Data/digit-recognizer/train.csv')

        """ DO THE LOADING THE OLD FASHIONED WAY """
        df = data.df.copy()
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
        train_df, val_df = train_test_split(train_df, test_size=0.2, random_state=42)

        train_labels = np.array(train_df.pop('label'))
        bool_train_labels = train_labels != 0
        val_labels = np.array(val_df.pop('label'))
        test_labels = np.array(test_df.pop('label'))

        train_features = np.array(train_df)
        val_features = np.array(val_df)
        test_features = np.array(test_df)

        scaler = StandardScaler()
        train_features = scaler.fit_transform(train_features)

        val_features = scaler.transform(val_features)
        test_features = scaler.transform(test_features)

        train_features = np.clip(train_features, -5, 5)
        val_features = np.clip(val_features, -5, 5)
        test_features = np.clip(test_features, -5, 5)

        for individual in thispopulation.individuallist:
            np.testing.assert_array_equal(individual.train_features, train_features)
            np.testing.assert_array_equal(individual.train_labels, train_labels)
            np.testing.assert_array_equal(individual.test_features, test_features)
            np.testing.assert_array_equal(individual.test_labels, test_labels)
            np.testing.assert_array_equal(individual.val_features, val_features)
            np.testing.assert_array_equal(individual.val_labels, val_labels)
