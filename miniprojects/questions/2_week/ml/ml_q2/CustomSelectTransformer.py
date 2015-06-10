# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:04:19 2015

@author: rhmbp
"""

from sklearn import base

class CustomSelectTransformer (base.BaseEstimator, base.TransformerMixin):
    """Transforms stuff """
    
    def __init__(self):
        pass
    def fit(self, X, y=None):
        
        return self
        
    def transform(self, X):
        """Does the work """
        # tansform X here (select columns from the list)
        return
    