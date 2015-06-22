# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Tue Jun  9 15:23:27 2015
ml_lib.py

@author: rhmbp
"""

# #==============================================================================
# # ml_lib.py
# # A module of class definitions for the ml.py miniproject (week 2).
# #==============================================================================


from ml_config import * # # constants and file paths
import pandas as pd
from sklearn import base
from sklearn.externals import joblib


# # Defs for Common Functions
# #==============================================================================
def lst_import_json():
    """
    Downloads the yelp academic dataset & returns as a list of dicts.\n
    Parameters
    -----
    Return: a list of dicts \n
    """
    import simplejson as json

    lst_json_src = []

    with open(PATH_JSON) as f:
        for line in f:
            lst_json_src.append(json.loads(line))
    return lst_json_src



# # Defs for Q2
# #==============================================================================

def worker_q2 (record, trained_model):
    """
    Applies K Nearest Neighbors to a list of dicts, based on a previously trained model.\n
    Returns: a 1d list of numpy.float64 \n
    Parameters \n
    ----- \n
    record: a list of dicts \n
    trained_model: a trained sklearn KNN model
    """
    # # 1) Subset features from testing data set
    features = X_FEATURES_Q2  # # must match list in ml_q2_trainer.py

    t = TransformerQ2()
    df_X = t.transform_X(record, features)

    # # 2) Convert pandas objects to array-like of floats
    df_X = df_X.applymap(float)
    df_X = df_X.as_matrix(columns=['latitude', 'longitude'])

    # # 3) Feed test set into the Kn predictor
    # # knregr = joblib.load(PATH_PKL_Q2)  # # do this in the Q2Class constructor
    knregr = trained_model

    y_pred = knregr.predict(df_X)  # # 1d lsit of np.float64
    y_pred = [float(i) for i in y_pred]  # convert types to float
    return y_pred[0]

# # ---------------

class TransformerQ2(base.BaseEstimator, base.TransformerMixin):
    """
    Transformer to subset features from records
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        # # rarely used, and def not used here
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
        # # handle single dicts
        tp = type(X)
        try:
            if tp == dict:  # # this condition (1 record) currently breaks in method, but not in ipython
                df_X = pd.DataFrame(X, columns=features, index=[0])
            else:
                df_X = pd.DataFrame(X, columns=features)
        except:
            print """Unrecognized input type, or Unrecognized feature. X should
            be a dict or list of dicts. Every feature passed must be a key in X.
            """
            return None
        return df_X

    def transform_Xy(self, X, feature_y):
        """
        Separates the feature that will become the label from a dataset.
        Stores array X and list y in obj.X and obj.y  Typically called after transform_X

        Returns: boolean \n
        Parameters \n
        -----\n
        X: a pandas DataFrame
        feature_y: string name of the column to separate
        """

        try:
            # # assign label column to y
            self.y = X[feature_y]

            # # strip label column from X
            features = list(X.columns)
            features.remove(feature_y)
            self.X = X[features]
        except:
            print """Something went wrong when trying to strip y from X in
            TransformeQ2, lines 66-73.
            """
            return False

        # # cast to array-like of float
        self.X = self.X.applymap(float).as_matrix(columns=['latitude', 'longitude'])
        self.y = list(self.y.apply(float))
        return True

    def transform(self, X, features_X, feature_y):
        """
        Convenience function to transform and strip X,y
        """
        self.transform_Xy(self.transform_X(X, features_X), feature_y)
        return True

# # ---------------

# #Defs for Q3
# #==============================================================================


def worker_q3(record, trained_model):
    """
    Applies feature extraction, then linear regression to a categorical feature set.\n

    Returns: a 1d list of numpy.float64 \n
    Parameters \n
    ----- \n
    record: a list of dicts \n
    trained_model:
    """
    from sklearn.feature_extraction import DictVectorizer

     # # 1) Subset features from testing data set
    features = X_FEATURE_Q3  # # must match list in ml_q3_trainer.py

    t = TransformerQ3()
    lst_dct_bool_cat = t.flatten(record, features) # convert X to boolean form

    v = DictVectorizer(sparse=False)  # create the feature extractor
    X = v.fit_transform(lst_dct_bool_cat)  # One Hot Encode the feature set

    # # 2) Run the regression
    lnrgr = trained_model
    y_pred = lnrgr.predict(X) # run the regression
    y_pred = [float(i) for i in y_pred]  # convert types to float
    return y_pred[0]

# # ---------------

class TransformerQ3(base.BaseEstimator, base.TransformerMixin):
    """
    Transformer to subset features from records
    """

    def __init__(self):
        pass

    def flatten(self, record, feature):
        """
        Converts dictionary keys with many categorical values into boolean form.\n
        Prepares a set of records for input into feature_extraction.DictVectorizer.\n
        Returns: A list of feature records with form { Doctor:1, Restaurant:0, .... }

        Parameters\n
        -------\n
        record: a single dictionary or list of dictionaries\n
        feature: the string name of a key
        """

        # 0) Handle single length records
        if type(record) == dict:
            #print "It's a dict", "(ml_lib.py: TransformerQ3::flatten(), line 210 )"
            record = [record]  # cast dict to list

        # 1) Get list of all possibile 'categories' values ###
        df_cat = pd.DataFrame(record, columns=[feature]) # extract feature: value for all records
        srs_cat = df_cat[feature]  # cast df to Series for convenience

        lst_cat_all = []
        for each_list in srs_cat:  # build list of all categories values
            for each_category in each_list:
                lst_cat_all.append(each_category)

        # 2) Extract the unique categories values (strings) ###
        srs_cat_unique = pd.Series((pd.Series(lst_cat_all)).unique())  # extract unique categories to Series

        # 3) Convert category lists to boolean form ###
        lst_dct_onehot = []
        for each_list in srs_cat: # for each record of source, build {categoryA: 0, categoryB: 0, . . . } w/ category = 1
            dct_copy = {cat: 0 for cat in srs_cat_unique} # initialize 1 empty dict via dict comprehension:  {categoryA: 0, categoryB: 0, . . . }
            for each_cat in each_list:
                dct_copy[each_cat] = 1  # flip the bit for each category in the list (cat that the business fits)
            lst_dct_onehot.append(dct_copy)

        return lst_dct_onehot

    def fit(self, X, y=None):
        # # rarely used, and def not used here
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
        try:
            df_X = pd.DataFrame(X, columns=features)
        except:
            print """Can't convert list to dataframe. Input must be a list of dicts.
            """
            return None

        return df_X

    def transform_Xy(self, X, feature_y):
        """
        Separates the feature that will become the label from a dataset.
        Stores array X and list y in obj.X and obj.y  Typically called after transform_X

        Returns: boolean \n
        Parameters \n
        -----\n
        X: a pandas DataFrame
        feature_y: string name of the column to separate
        """

        try:
            # # assign label column to y
            self.y = X[feature_y]

            # # strip label column from X
            features = list(X.columns)
            features.remove(feature_y)
            self.X = X[features]
        except:
            print """Something went wrong when trying to strip y from X in
            TransformerQ4
            """
            return False

        # # cast to array-like
        self.X = self.X.as_matrix(columns=['categories'])
        self.y = list(self.y.apply(float))

        return True

    def transform(self, X, features_X, feature_y):
        """
        Convenience function to transform and strip X,y
        """
        self.transform_Xy(self.transform_X(X, features_X), feature_y)
        return True



# # ---------------



# # ---------------