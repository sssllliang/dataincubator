# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:23:27 2015

@author: rhmbp
"""

#==============================================================================
# ml_lib.py
# A module of class definitions for the ml.py miniproject (week 2). 
#==============================================================================

from sklearn import base

# Defs for Q1: CityModel
#==============================================================================
class EstimatorQ1(base.BaseEstimator, base.ClassifierMixin):
     
     def __init__(self):
         # initialization code
         return
     
     def fit(self, X, y):
         """X = list, y = list.
             Aggregates mean score by city & creates a pandas GroupBy obj """
         # fit the model ...
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
         
         self.hyp = df_avg_bycity
         
         return self.hyp
     
     
     def predict(self, X):
         df = self.hyp
         y_pred = []
         
         for row in X:
             stars = df.loc[df['cities']==row,'avgstars']
             y_pred.append(stars)
         
         self.pred = y_pred
        
         return self.pred # prediction
         

         

#==============================================================================        
# END Q1        
        