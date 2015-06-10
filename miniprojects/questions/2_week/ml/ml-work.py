# ml-work.py

# #!/bin/bash
# 
# cd ~/miniprojects/questions/2-week/ml/data
# wget http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_business.json.gz
#
# gunzip yelp_train_academic_dataset_business.json.gz
# 

# file is a collection of json-formatted dicts; each line looks like:
#==============================================================================
# {
# 	"business_id": "vcNAWiLM4dR7D2nwwJ7nCA", 
# 	"full_address": "4840 E Indian School Rd\nSte 101\nPhoenix, AZ 85018", 
# 	"hours": {"Tuesday": {"close": "17:00", "open": "08:00"}, 
# 	          "Friday": {"close": "17:00", "open": "08:00"}, 
# 		    "Monday": {"close": "17:00", "open": "08:00"}, 
# 		    "Wednesday": {"close": "17:00", "open": "08:00"}, 
# 		    "Thursday": {"close": "17:00", "open": "08:00"}
# 		   }, 
# 	"open": true, 
# 	"categories": ["Doctors", "Health & Medical"], 
# 	"city": "Phoenix", "review_count": 7, 
# 	"name": "Eric Goldberg, MD", 
# 	"neighborhoods": [], 
# 	"longitude": -111.98375799999999, 
# 	"state": "AZ", 
#     "stars": 3.5, 
# 	"latitude": 33.499313000000001, 
# 	"attributes": {"By Appointment Only": true}, 
#	"type": "business"
# }
#==============================================================================


# imports
#==============================================================================
#%matplotlib inline
import matplotlib
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 2 * matplotlib.rcParams['savefig.dpi']
import simplejson as json
import sklearn
import pandas as pd
from Estimator import Estimator
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

#lst_yelp = lst_import_yelp()   
#print len(lst_yelp)
#print lst_yelp[0]    


# load 1 record into processing list
record = {'city':'Phoenix', 'stars':3.5}
record = pd.DataFrame(record, index=[0])

X = list(record['city'])
y = list(record['stars'])




# test estimator
#==============================================================================
cls = Estimator()

X_train = X_test = X = ['lv', 'nyc', 'la', 'la', 'la', 'nyc', 'lv', 'la','lv', 'nyc', 'la', 'nyc', 'la',]
y_train = y_test = y = [1,2,3,4,5,6,7,8,9,10,11,12,13]

cls.fit(X_train, y_train)  # fit data

y_pred = cls.predict(X_test)  # predict answer

#print X_test.shape, y_test.shape
#cls.score((X_test, y_test)  # this part is bullshit
print y_pred


#==============================================================================


			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
