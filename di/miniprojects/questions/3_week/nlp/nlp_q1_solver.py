# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Mon Jun 14 01:37:23 2015

nlp_q1_trainer.py


@author: rhmbp
"""

mport numpy as np
import random
import simplejson as json

from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import random


import nlp_lib
from nlp_config import *


# 1) load the json data
lst_reviews = []
lst_stars = []

i = 0  # counter
lst_sample_mask = random.sample(range(1,4000),3000)

# build feature lists from random rows
with open("/home/vagrant/miniprojects/questions/3_week/nlp/data/tiny_review.json") as f:
    for line in f:
        if i in lst_sample_mask:
            tmp = json.loads(line)
            lst_reviews.append(tmp['text'])
            lst_stars.append(tmp['stars'])
        i += 1
## reviews come out tokenized- each review is 1 string
print len(lst_stars), "reviews"


# 2) bag of words
from sklearn.feature_extraction.text import CountVectorizer

bag_of_words_vectorizer = CountVectorizer(stop_words=nltk.corpus.stopwords.words('english'))

counts = bag_of_words_vectorizer.fit_transform(lst_reviews)
X_trn = counts
#print counts.shape

## 5 reviews, 146 uniques words


# 3) #train the classifier
clf = MultinomialNB().fit(X_trn, lst_stars)

# 4) save the model
joblib.dump(clf, PATH_PKL_Q1)

