# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:24:31 2015
ml_q4_trainer.py

@author: rhmbp
"""

from .. import ml_lib


import simplejson as json
import pandas as pd
from sklearn.externals import joblib
from EstimatorQ1 import EstimatorQ1



## load a training set ##

# import the json file
df_X = pd.DataFrame(lst_import_json())

X = list(df_record.city)
y = list(df_record.stars)

cest_star_rating = EstimatorQ1()

cest_star_rating.fit(X, y)  # fit data

joblib.dump(cest_star_rating, '/home/vagrant/miniproject/questions/2_week/ml/pickles/q1_model.pkl')
from EstimatorQ4 import EstimatorQ4

