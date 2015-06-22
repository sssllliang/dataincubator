# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Tue Jun  9 15:23:27 2015

Saves a trained estimator object for ml.Q1
Run from cmd with python
@author: rhmbp
"""

#==============================================================================
# ml_q1_worker.py
# A module of class definitions for the ml.py miniproject (week 2). 
#==============================================================================

## imports ##
import os
import pandas as pd
from sklearn.externals import joblib
import EstimatorQ1 as EstimatorQ1



def calc_y_pred(record):
    """Loads a trained model, then runs the predict method & returns a vector of predicted labels"""
    # convert dict input into lists
    # cest = joblib.load('/home/vagrant/miniproject/questions/2_week/ml/pickles/q1_model.pkl')
    cest = joblib.load(os.path.realpath('questions/2_week/ml/pickles/q1_model.pkl'))

    if type(record) == dict:
        df_record = pd.DataFrame(record, index=[0])
    elif type(record) == list:
        df_record = pd.DataFrame(record)
    else:
        df_record =  pd.DataFrame({'city':'Phoenix', 'stars':4})
        print "X is not list or dict, defaulting to dummy input"

    X = list(df_record.city)
    #y = list(df_record.stars)

    y_pred = cest.predict(X)[0]  # predict answer
    y_pred = float(list(y_pred)[0])

    return y_pred











