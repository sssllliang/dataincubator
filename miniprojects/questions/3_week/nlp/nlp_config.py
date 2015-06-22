# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Mon Jun 14 01:36:52 2015

nlp_config.py


@author: rhmbp
"""

# path to small test set of yelp reviews
PATH_NLP = '/Users/rhmbp/Dev/Data_Incubator/miniprojects/questions/3_week/nlp/'
PATH_NLP = '/home/vagrant/miniprojects/questions/3_week/nlp/'

PATH_TINY = PATH_NLP + 'data/tiny_review.json'

# path to data set
PATH_REVIEW = PATH _NLP+ 'data/yelp_train_academic_dataset_review.json'

# path to yelp business data for Q3
PATH_BUSINESS = ''

PATH_PKL = PATH_NLP + 'pickles/'



# Q1 Parameters
#==============================================================================
X_FEATURES_Q1 = ['text', 'stars']  # features for the CustomSelectTransformer to extract
Y_FEATURE_Q1 = 'stars'  # name of the column to use for y
PATH_PKL_Q1 = PATH_PKL + 'q1_model.pkl'  # location of the pickled trained model files



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