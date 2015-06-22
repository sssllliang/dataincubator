# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 01:36:52 2015
ml_q3_trainer.py CategoryModel

Trains a K Nearest Neighbors Regressor from a json source file.

@author: rhmbp
"""
from ml_lib import lst_import_json, TransformerQ3, worker_q3, get_cats
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from ml_config import X_FEATURE_Q3, PATH_PKL_Q3, LST_ALL_CATS
import numpy as np
# 1) Import & load the json file  ###
record = []
record = lst_import_json()

# 2) Convert category feature regressable form (One Hot Encoded)  ###
LST_ALL_CATS = get_cats()

t = TransformerQ3()
lst_dct_bool_cat = t.flatten(record, X_FEATURE_Q3, LST_ALL_CATS) # convert X to boolean form

#==============================================================================
# At this point, lst_dct_bool is a list of all category records, with a
# boolean form dict for each record. DictVectorizer can take this form
# lst_dct_bool_cat => [{ Doctor:1, Restaurant:0, .... }]
#==============================================================================

v = DictVectorizer(sparse=False)  # create the feature extractor
X = v.fit_transform(lst_dct_bool_cat)  # One Hot Encode the feature set

# 3) Train a linear model
t.transform(record, ['categories', 'stars'], 'stars') # create the y_trn vector (in t.y)

lnrgr = LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)

lnrgr.fit(X,t.y) # train the model

joblib.dump(lnrgr, PATH_PKL_Q3)
