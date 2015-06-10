# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:04:19 2015

@author: rhmbp
"""

transformer = Transformer(...)  # initialize
X_trans_train = transformer.fit_transform(X_train)  # fit / transform data
estimator.fit(X_trans_train, y_train)  # fit new model on training data
X_trans_test = transformer.transform(X_test)  # transform test data
estimator.score(X_trans_test, y_test)  # fit new model