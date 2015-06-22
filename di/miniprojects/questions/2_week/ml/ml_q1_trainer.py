# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Tue Jun  9 19:28:37 2015

ml_q1_trainer.py
Saves a trained estimator object for ml.Q1

@author: rhmbp
"""

import simplejson as json
import pandas as pd
from sklearn.externals import joblib
from EstimatorQ1 import EstimatorQ1

# Definitions
#===============================================================================
def lst_import_yelp():
    """Returns a list of json-formatted dicts"""
    path = 'data/yelp_train_academic_dataset_business.json'

    lst_json_src = []
    with open(path) as f:
        for line in f:
            lst_json_src.append(json.loads(line))
    return lst_json_src


## load a training set ##

# import the json file
record = lst_import_yelp()

## convert record to lists ##
df_record = pd.DataFrame(record)

X = list(df_record.city)
y = list(df_record.stars)

cest_star_rating = EstimatorQ1()

cest_star_rating.fit(X, y)  # fit data

joblib.dump(cest_star_rating, '/home/vagrant/miniproject/questions/2_week/ml/pickles/q1_model.pkl')
from EstimatorQ1 import EstimatorQ1

