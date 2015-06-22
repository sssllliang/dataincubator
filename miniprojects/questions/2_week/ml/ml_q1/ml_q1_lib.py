# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:23:27 2015

@author: rhmbp
"""

#==============================================================================
# ml_lib.py
# A module of class definitions for the ml.py miniproject (week 2). 
#==============================================================================

## imports ##
import simplejson as json
from sklearn import base
import pandas as pd


## this code should run when the module is imported ##

# convert dict input into lists          
record = {'city':'Phoenix', 'stars':3.5}
record = pd.DataFrame(record, index=[0])

X = list(record['city'])
y = list(record['stars'])

X_train = X_test = X
cest_rating = Estimator()

cest_rating.fit(X_train, y_train)  # fit data

y_pred = cest_rating.predict(X_test)  # predict answer

print y_pred


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

#
# END class EstimatorQ1
#==============================================================================        
         

# import the json file
def lst_import_yelp():
    """Returns a list of json-formatted dicts"""
    path = './data/yelp_train_academic_dataset_business.json'

    lst_json_src = []
    with open(path) as f:
        for line in f:
            lst_json_src.append(json.loads(line))
    return lst_json_src
         

#==============================================================================        
# END Q1        
        