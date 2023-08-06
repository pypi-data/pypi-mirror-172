from src.Dataset import Dataset
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import unittest

class TestDataset(unittest.TestCase):
    def test_load_data(self):
        data = Dataset('Data/digit-recognizer/train.csv')
        loadeddf = data.df
        testdata = pd.read_csv('Data/digit-recognizer/train.csv')
        pd.testing.assert_frame_equal(loadeddf, testdata)

    def test_update_classification(self):
        data = Dataset('Data/digit-recognizer/train.csv')
        testdata = data.df.copy()
        randarray = pd.Series(np.random.rand(testdata.shape[0]))
        testdata["Classification"] = randarray
        data.updateClassification(randarray)
        areequal = True if data.df["Classification"].equals(testdata["Classification"]) else False
        self.assertTrue(areequal)

    def test_load_deep_neural_net_data(self):
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

        """ COMPARE TO DATASET'S BUILT IN FUNCTION """
        data.loaddeepneuralnetdata()
        train_features_test, train_labels_test, test_features_test, test_labels_test, val_features_test, val_labels_test = data.grabneuralnetdata()
        np.testing.assert_array_equal(train_features, train_features_test)
        np.testing.assert_array_equal(train_labels, train_labels_test)
        np.testing.assert_array_equal(test_features, test_features_test)
        np.testing.assert_array_equal(test_labels, test_labels_test)
        np.testing.assert_array_equal(val_features, val_features_test)
        np.testing.assert_array_equal(val_labels, val_labels_test)

