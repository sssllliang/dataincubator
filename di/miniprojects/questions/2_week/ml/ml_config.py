# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:44:24 2015

@author: rhmbp
"""

# Common Parameters
#==============================================================================

## path to your working directory
PATH_ML = '/home/vagrant/miniprojects/questions/2_week/ml'
#PATH_ML = '/Users/rhmbp/Dev/Data_Incubator/miniprojects/questions/2_week/ml/'

## path to the source json file (for training)
PATH_JSON = '/home/vagrant/miniprojects/questions/2_week/ml/data/yelp_train_academic_dataset_business.json'
#PATH_JSON = '/Users/rhmbp/Dev/Data_Incubator/miniprojects/questions/2_week/ml/data/yelp_train_academic_dataset_business.json'

# general path to your (pickled) trained models
PATH_PKL = '/home/vagrant/miniprojects/questions/2_week/ml/pickles/'
#PATH_PKL ='/Users/rhmbp/Dev/Data_Incubator/miniprojects/questions/2_week/ml/pickles/'


# Q2 Parameters
#==============================================================================
X_FEATURES_Q2 = ['latitude', 'longitude', 'stars']  # features for the CustomSelectTransformer to extract
Y_FEATURE_Q2 = 'stars'  # name of the column to use for y
PATH_PKL_Q2 = PATH_PKL + 'q2_model.pkl'  # location of the pickled trained model files


# Q3 Parameters
#==============================================================================
X_FEATURE_Q3 = 'categories'
Y_FEATURE_Q2 = 'stars'  # name of the column to use for y
PATH_PKL_Q3 = PATH_PKL + 'q3_model.pkl'

# Q4 Parameters
#==============================================================================



# Q5 Parameters
#==============================================================================