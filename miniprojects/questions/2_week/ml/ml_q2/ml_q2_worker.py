# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:04:19 2015
ml_q2_worker.py

Calculate labels for a data set by loading a previously trained model

@author: rhmbp
"""

# model is already trained

from ml_lib import *


# 1) Import & load a testing set
record = []
record = lst_import_json()

# 2) Select features
features = ml_config.CONST_Q2_X_FEATURES  # must match list in ml_q2_trainer.py

t = TransformerQ2()
df_X = t.transform_X(record,features)


# 3) Convert pandas objects to array-like of floats
df_X = df_X.applymap(float)
df_X = df_X.as_matrix(columns=['latitude','longitude'])

# 4) Feed array into the Kn predictor
knregr = joblib.load('/Users/rhmbp/Dev/Data_Incubator/miniprojects/questions/2_week/ml/pickles/q2_model.pkl')

y_pred = knregr.predict(df_X)  # 1d lsit of np.float64

### cross validate somewhere in here