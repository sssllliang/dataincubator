# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:07:54 2015

@author: rhmbp
"""
from sklearn import base

class Estimator(base.BaseEstimator, base.ClassifierMixin):
    def __init__(self):
        # initialization code
        return
    
    def fit(self, X, y):
        """X = list, y = list.
            Aggregates mean score by city & creates a pandas GroupBy obj """
        # fit the model ...
        # initialize output df
        from numpy import NaN
        import pandas as pd
        
        X = pd.Series(X) 
        
        y = pd.Series(y) 
        
        df_yelp = pd.DataFrame()
        
        df_yelp['cities'] = X
        df_yelp['stars'] = y
        
        dfg_yelp = df_yelp.groupby('cities')
        
        lst_cities = []
        lst_avgstars = []
        
        for city, df_stars_by_city in dfg_yelp:
            mn = df_stars_by_city.stars.mean()
            lst_cities.append(city)
            lst_avgstars.append(mn)
            
        df_avg_bycity = pd.DataFrame()
        df_avg_bycity['cities'] = lst_cities
        df_avg_bycity['avgstars'] = lst_avgstars
        
        return self
        
    def predict(self, X):
        return # prediction

    
    