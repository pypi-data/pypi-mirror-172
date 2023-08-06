import pandas as pd


from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import StandardScaler


class Dataset:
    """
    All purpose modular Dataset Object for Blacklight. Built on Pandas base. Includes Feature selection, Feature scaling, and writing by output.
    """
    def __init__(self, inputfilelocation, isclassified=False, json=False):
        """
        Takes an input file, and if the data coming in has classification or not. Classification must be
        in the last column and have the columnname 'Classification'
        :param inputfilelocation:
        :param isclassified:
        """
        if json:
            self.df = pd.read_json(inputfilelocation, orient='records')
        else:
            self.df = pd.read_csv(inputfilelocation)
        if isclassified:
            self.values = self.df.iloc[:, :-1]
            self.target = self.df.iloc[:, -1]
        else:
            self.values = self.df

    def updateClassification(self, Classification):
        self.df['Classification'] = Classification

    def writeOutput(self, outputloc):
        """
        Writes output to json file located at OUTPUTLOC.
        :param outputloc:
        :return:
        """
        self.df.to_json(outputloc, orient='records', indent=4)

    def scaletoColumnbyValue(self, columnName, newcolumnvalue):
        """
        Scales all values in each row of df by ColumnName to ColumnValue, returing a class attribute scaledvalues.
        :param columnName:
        :param newcolumnvalue:
        :return:
        """
        scaleddf = self.values.apply(lambda row: row * (newcolumnvalue / row[columnName]), axis=1)
        self.scaledvalues = scaleddf

    def loaddeepneuralnetdata(self):
        """
        Loads data from self.inputloc, then creates testing, training, and validation data.
        """
        df = self.df
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
        self.train_features = train_features
        self.train_labels = train_labels
        self.test_features = test_features
        self.test_labels = test_labels
        self.val_features = val_features
        self.val_labels = val_labels

    def grabneuralnetdata(self):
        return self.train_features, self.train_labels, self.test_features, self.test_labels, self.val_features, self.val_labels