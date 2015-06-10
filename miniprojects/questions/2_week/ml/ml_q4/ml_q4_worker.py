# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:19:32 2015

@author: rhmbp
"""



# import giulio's custom transformer
t = transformer()
X_trans = t.transform(X)

# send transformed X into DictVectorizer (flattens more)
X_trans_vect = sk.DictVectorizer(X_trans)

## the above process simply unpacks (flattens) nested dicts 

# send goodified X to a custom linear model that is cross validated
# --> def fit(X): return sk.linearModel(sk.CrossValidate(X))
e = Estimator()

e.fit(X_trans_vect,y)

# use model to predict labels

y_predicted = e.predict(X_train)