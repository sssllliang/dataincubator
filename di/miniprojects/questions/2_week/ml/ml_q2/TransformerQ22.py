# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:04:19 2015
TransformerQ2.py

@author: rhmbp
"""

import pandas as pd
from sklearn import base


class TransformerQ2(base.BaseEstimator, base.TransformerMixin):
    """
    Transformer to subset features from records
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        # rarely used, and df not used here
        return self

    def transform_X(self, X, features):
        """
        Subsets dicts by key name & returns a dataframe with features as
        columns.\n

        Returns: a pandas DataFrame \n
        Parameters \n
        -----\n
        X: a list of dicts, \n
        features: a list of string dict key names \n
        """

        # handle single dicts
        tp = type(X)
        try:
            if tp == dict: # this condition (1 record) currently breaks in method, but not in ipython
                df_X = pd.DataFrame(X, columns=features, index=[0])
            else:
                df_X = pd.DataFrame(X, columns=features)
        except :
            print """Unrecognized input type, or Unrecognized feature. X should
            be a dict or list of dicts. Every feature passed must be a key in
            X.
            """
            return None
        return df_X

    def transform_Xy(self, X, feature_y):
        """
        Separates the feature that will become the label from a dataset.
        Stores X and y in obj.X and obj.y  Typically called after transform_X

        Returns: boolean \n
        Parameters \n
        -----\n
        X: a pandas DataFrame
        feature_y: string name of the column to separate
        """

        try:
            # assign label column to y
            self.y = X[feature_y]

            # strip label column from X
            features = list(X.columns)
            features.remove(feature_y)
            self.X = X[features]
        except:
            print """Something went wrong when trying to strip y from X in 
            Transformer Q2, lines 66-73.
            """
            return False

        return True
        



