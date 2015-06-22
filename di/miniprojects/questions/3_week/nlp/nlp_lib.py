# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Mon Jun 14 01:37:23 2015

nlp_lib.py


@author: rhmbp
"""

from mlp_config import *

# Common Defs
#==============================================================================
def lst_import_json():
    """
    Downloads the yelp academic dataset & returns as a list of dicts.\n
    Parameters
    -----
    Return: a list of dicts \n
    """
    import simplejson as json

    lst_json_src = []

    with open(PATH_REVIEW) as f:
        for line in f:
            lst_json_src.append(json.loads(line))
    return lst_json_src

	"""
    Converts dictionary keys with many categorical values into boolean form.\n
    Prepares a set of records for input into feature_extraction.DictVectorizer.\n
    Returns: A list of feature records with form { Doctor:1, Restaurant:0, .... }

    Parameters\n
    -------\n
    record: a single dictionary or list of dictionaries\n
    feature: the string name of a key
    """

    # 0) Handle single length records
    if type(record) == dict:
        #print "It's a dict", "(ml_lib.py: TransformerQ3::flatten(), line 210 )"
        record = [record]  # cast dict to list

    # 1) Get list of all possibile 'categories' values ###
    df_cat = pd.DataFrame(record, columns=[feature]) # extract feature: value for all records
    srs_cat = df_cat[feature]  # cast df to Series for convenience

    lst_cat_all = []
    for each_list in srs_cat:  # build list of all categories values
        for each_category in each_list:
            lst_cat_all.append(each_category)

    # 2) Extract the unique categories values (strings) ###
    srs_cat_unique = pd.Series((pd.Series(lst_cat_all)).unique())  # extract unique categories to Series

    # 3) Convert category lists to boolean form ###
    lst_dct_onehot = []
    for each_list in srs_cat: # for each record of source, build {categoryA: 0, categoryB: 0, . . . } w/ category = 1
        dct_copy = {cat: 0 for cat in srs_cat_unique} # initialize 1 empty dict via dict comprehension:  {categoryA: 0, categoryB: 0, . . . }
        for each_cat in each_list:
            dct_copy[each_cat] = 1  # flip the bit for each category in the list (cat that the business fits)
        lst_dct_onehot.append(dct_copy)

    return lst_dct_onehot

def df_extract_features(record, features):
	"""
	Subsets dicts by key name & returns a dataframe with features as columns.\n

    Returns: a pandas DataFrame \n
    Parameters \n
    -----\n
    record: a list of dicts, \n
    features: a list of string dict key names \n
	"""

	return


# Q1 Defs
#==============================================================================

def q1_worker():

	 #1) load the json data


	# 2) filter the review text and star keys

	# 2a) separate the rows by star rating
	lst_str_good = []
	lst_str_bad = []


	# 3) parse data - each review is 1 string (a document)


	# 4) tokenize review text with CountVectorizer
	bag_of_words_vectorizer = CountVectorizer()

	# feed the list of strings directly into the vectorizer; it will count each sentence
	word_counts = bag_of_words_vectorizer.fit_transform(  lst_str_good+lst_str_bad )

	# shape shows that ____ different words have been used in ____ reviews
	print word_counts.shape

	# 5) load a model

	# 6) feed the tokenized data into the model (predict)




# Q2 Defs
#==============================================================================





#Q3 Defs
#==============================================================================