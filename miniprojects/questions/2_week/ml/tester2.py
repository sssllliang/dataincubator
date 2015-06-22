# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 01:36:52 2015


@author: rhmbp
"""

from ml_lib import lst_import_json, TransformerQ2
from ml_config import *
import numpy as np


## 1) load test set
record = []
record = lst_import_json()


t = TransformerQ2()
df_X = t.transform_X(record, X_FEATURES_Q2)
# split off the y feature
t.transform_Xy(df_X, Y_FEATURE_Q2)  # saves X, y to t.X, t.y

# split set into training and testing sets
from sklearn.cross_validation import train_test_split
X_trn, X_tst, y_trn, y_tst = train_test_split(t.X, t.y, test_size=0.33, random_state=42)


# grid search
#from sklearn.grid_search import GridSearchCV
from sklearn import neighbors, grid_search

knr = neighbors.KNeighborsRegressor()
knr_params = {'n_neighbors':[ 130,131,132], 'leaf_size':[50]}
gsc = grid_search.GridSearchCV(knr, knr_params)
gsc.fit(X_trn, y_trn)

#print gsc.grid_scores_,'\n'
print 'best estimator', gsc.best_estimator_, '\n'
print 'best score', gsc.best_score_, '\n'
print 'best params', gsc.best_params_, '\n'

knrb = gsc.best_estimator_

y_pred = knrb.predict(X_tst)
print knrb.score(X_tst,y_tst),'\n'

print gsc.score(X_tst,y_tst), '\n'


#
## 2) Call worker function to transform input & calculate labels
#q2 = Q2Class()
#y_pred = q2.solve(record)  # this should really be a pipeline
#
#print y_pred[0:5]
