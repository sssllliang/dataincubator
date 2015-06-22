# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 01:36:52 2015
ml_q2_trainer.py

Trains a K Nearest Neighbors Regressor from a json source file.

@author: rhmbp
"""
from ml_lib import lst_import_json, TransformerQ2
from ml_config import X_FEATURES_Q2, Y_FEATURE_Q2, PATH_PKL_Q2
from sklearn import neighbors, grid_search
from sklearn.externals import joblib
import pandas as pd

# 1) import & load the json file
record = []
record = lst_import_json()


# 2) create the custom transformer & select your features
try:
    t = TransformerQ2()
except:
    print "transformer failed"

features = X_FEATURES_Q2  # must match list in ml_q2_worker.py

t.transform(record, X_FEATURES_Q2, Y_FEATURE_Q2)

print type(t.X), type(t.y)




# 3) Train the model
knregr = neighbors.KNeighborsRegressor()  # create the regressor object
knr_params = {'n_neighbors':[ 130,131,132], 'leaf_size':[50]}

gsc = grid_search.GridSearchCV(knr, knr_params)

gsc.fit(t.X, t.y)  # train the model

# 5) Save the trained model
joblib.dump(gsc.best_estimator_, PATH_PKL_Q2)

print '\n\n', gsc.best_estimator_, '\n\n', gsc.best_score_, '\n\n'
