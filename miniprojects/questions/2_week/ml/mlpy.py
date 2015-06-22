# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Thu Jun 11 01:36:52 2015


@author: rhmbp
"""




class Q2Class():
    def __init__(self):

        # import the joblib fcn & path to pickled model
        from sklearn.externals import joblib
        from ml_config import PATH_PKL_Q2

        # load the trained model into the global scope
        self.model = joblib.load(PATH_PKL_Q2)
        return

    def solve(self, record):
        from ml_lib import worker_q2
        y_pred = worker_q2(record, self.model)
        return y_pred


class Q3Class():
    def __init__(self):

        # import the joblib fcn & path to pickled model
        from sklearn.externals import joblib
        from ml_config import PATH_PKL_Q3

        # load the trained model into the global scope
        self.model = joblib.load(PATH_PKL_Q3)
        return


    def solve(self, record):
        from ml_lib import worker_q3

        record = [{"categories": ["Doctors", "Health & Medical"]}]
#        record = [{"categories": ["Doctors", "Health & Medical"]}, {"categories": ["Restaurants"]}, {"categories": ["American (Traditional)", "Restaurants"]}]
        y_pred = worker_q3(record, self.model)
        print y_pred
        return y_pred

## 1) load test set
#record = []
#record = lst_import_json()
#
## 2) Call worker function to transform input & calculate labels
#q2 = Q2Class()
#y_pred = q2.solve(record)  # this should really be a pipeline
#
#print y_pred[0:5]
