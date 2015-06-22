"""
## Overview

Our objective is to predict a new venue's popularity from information available when the venue opens.  We will do this by machine learning from a dataset of venue popularities provided by Yelp.  The dataset contains meta data about the venue (where it is located, the type of food served, etc ...).  It also contains a star rating.  This tutorial will walk you through one way to build a machine-learning algorithm.

## Metric

Your model will be assessed based on the root mean squared error of the number of stars you predict.  There is a reference solution (which should not be too hard to beat).  The reference solution has a score of 1.

## Download and parse the incoming data

[link](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_business.json.gz)

Notice that each row of the file is a json blurb.  You can read it in python.  *Hints:*
1. `gzip.open` ([docs](https://docs.python.org/2/library/gzip.html)) has the same interface as `open` but is for `.gz` files.
2. `simplejson` ([docs](http://simplejson.readthedocs.org/en/latest/)) has the same interface as `json` but is *substantially* faster.

## Setup cross-validation:
In order to track the performance of your machine-learning, you might want to use `cross_validation.train_test_split` ([docs](http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.train_test_split.html)).


## Building models in sklearn

All estimators (e.g. linear regression, kmeans, etc ...) support `fit` and `predict` methods.  In fact, you can build your own by inheriting from classes in `sklearn.base` by using this template:
``` python
class Estimator(base.BaseEstimator, base.RegressorMixin):
  def __init__(self, ...):
   # initialization code

  def fit(self, X, y):
    # fit the model ...
    return self

  def predict(self, X):
    return # prediction
```
The intended usage is:
``` python
estimator = Estimator(...)  # initialize
estimator.fit(X_train, y_train)  # fit data
y_pred = estimator.predict(X_test)  # predict answer
estimator.score(X_test, y_test)  # evaluate performance
```
The regressor provides an implementation of `.score`.  Conforming to this convention has the benefit that many tools (e.g. cross-validation, grid search) rely on this interface so you can use your new estimators with the existing `sklearn` infrastructure.

For example `grid_search.GridSearchCV` ([docs](http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html)) takes an estimator and some hyperparameters as arguments, and returns another estimator.  Upon fitting, it fits the best model (based on the inputted hyperparameters) and uses that for prediction.

Of course, we sometimes need to process or transform the data before we can do machine-learning on it.  `sklearn` has Transformers to help with this.  They implement this interface:
``` python
class Transformer(base.BaseEstimator, base.TransformerMixin):
  def __init__(self, ...):
   # initialization code

  def fit(self, X, y=None):
    # fit the transformation ...
    return self

  def transform(self, X):
    return ... # transformation
```
When combined with our previous `estimator`, the intended usage is
``` python
transformer = Transformer(...)  # initialize
X_trans_train = transformer.fit_transform(X_train)  # fit / transform data
estimator.fit(X_trans_train, y_train)  # fit new model on training data
X_trans_test = transformer.transform(X_test)  # transform test data
estimator.score(X_trans_test, y_test)  # fit new model
```
Here, `.fit_transform` is implemented based on the `.fit` and `.transform` methods in `base.TransformerMixin` ([docs](http://scikit-learn.org/stable/modules/generated/sklearn.base.TransformerMixin.html)).  Especially for transformers, `.fit` is often empty and only `.transform` actually does something.

The real reason we use transformers is that we can chain them together with pipelines.  For example, this
``` python
new_model = pipeline.Pipeline([
    ('trans', Transformer(...)),
    ('est', Estimator(...))
  ])
new_model.fit(X_train, y_train)
new_model.score(X_test, y_test)
```
would replace all the fitting and scoring code above.  That is, the pipeline itself is an estimator (and implements the `.fit` and `.predict` methods).  Note that a pipeline can have multiple transformers chained up but at most one (optional) terminal estimator.


## A few helpful notes about performance.

1. To deploy a model (get a trained model into Heroku), we suggest using the [`dill` library](https://pypi.python.org/pypi/dill) or [`joblib`](http://scikit-learn.org/stable/modules/model_persistence.html) to save it to disk and check it into git.  This allows you to train the model offline in another file but run it here by reading it in this file.  The model is way too complicated to be trained in real-time!

2. Make sure you load the `dill` file upon server start, not upon a call to `solution`.  This can be done by loaindg the model the model into the global scope.  The model is way too complicated to be even loaded in real-time!

3. Make sure you call `predict` once per call of `def solution`.  This can be done because `predict` is made to take a list of elements.

4. You probably want to use GridSearchCV to find the best hyperparameters by splitting the data into training and test.  But for the final model that you submit, don't forget to retrain on all your data (training and test) with these best parameters.
"""

from lib import (QuestionList, Question, list_or_dict, catch_validate_exception,
  YelpListOrDictValidateMixin)
QuestionList.set_name("ml")


class MLValidateMixin(YelpListOrDictValidateMixin, Question):
  @classmethod
  def fields(cls):
    return cls._fields

  @classmethod
  def _test_json(cls):
    return [
      {"business_id": "vcNAWiLM4dR7D2nwwJ7nCA", "full_address": "4840 E Indian School Rd\nSte 101\nPhoenix, AZ 85018", "hours": {"Tuesday": {"close": "17:00", "open": "08:00"}, "Friday": {"close": "17:00", "open": "08:00"}, "Monday": {"close": "17:00", "open": "08:00"}, "Wednesday": {"close": "17:00", "open": "08:00"}, "Thursday": {"close": "17:00", "open": "08:00"}}, "open": True, "categories": ["Doctors", "Health & Medical"], "city": "Phoenix", "review_count": 7, "name": "Eric Goldberg, MD", "neighborhoods": [], "longitude": -111.98375799999999, "state": "AZ", "stars": 3.5, "latitude": 33.499313000000001, "attributes": {"By Appointment Only": True}, "type": "business"},
      {"business_id": "JwUE5GmEO-sH1FuwJgKBlQ", "full_address": "6162 US Highway 51\nDe Forest, WI 53532", "hours": {}, "open": True, "categories": ["Restaurants"], "city": "De Forest", "review_count": 26, "name": "Pine Cone Restaurant", "neighborhoods": [], "longitude": -89.335843999999994, "state": "WI", "stars": 4.0, "latitude": 43.238892999999997, "attributes": {"Take-out": True, "Good For": {"dessert": False, "latenight": False, "lunch": True, "dinner": False, "breakfast": False, "brunch": False}, "Caters": False, "Noise Level": "average", "Takes Reservations": False, "Delivery": False, "Ambience": {"romantic": False, "intimate": False, "touristy": False, "hipster": False, "divey": False, "classy": False, "trendy": False, "upscale": False, "casual": False}, "Parking": {"garage": False, "street": False, "validated": False, "lot": True, "valet": False}, "Has TV": True, "Outdoor Seating": False, "Attire": "casual", "Alcohol": "none", "Waiter Service": True, "Accepts Credit Cards": True, "Good for Kids": True, "Good For Groups": True, "Price Range": 1}, "type": "business"},
      {"business_id": "uGykseHzyS5xAMWoN6YUqA", "full_address": "505 W North St\nDe Forest, WI 53532", "hours": {"Monday": {"close": "22:00", "open": "06:00"}, "Tuesday": {"close": "22:00", "open": "06:00"}, "Friday": {"close": "22:00", "open": "06:00"}, "Wednesday": {"close": "22:00", "open": "06:00"}, "Thursday": {"close": "22:00", "open": "06:00"}, "Sunday": {"close": "21:00", "open": "06:00"}, "Saturday": {"close": "22:00", "open": "06:00"}}, "open": True, "categories": ["American (Traditional)", "Restaurants"], "city": "De Forest", "review_count": 16, "name": "Deforest Family Restaurant", "neighborhoods": [], "longitude": -89.353437, "state": "WI", "stars": 4.0, "latitude": 43.252267000000003, "attributes": {"Take-out": True, "Good For": {"dessert": False, "latenight": False, "lunch": False, "dinner": False, "breakfast": False, "brunch": True}, "Caters": False, "Noise Level": "quiet", "Takes Reservations": False, "Delivery": False, "Parking": {"garage": False, "street": False, "validated": False, "lot": True, "valet": False}, "Has TV": True, "Outdoor Seating": False, "Attire": "casual", "Ambience": {"romantic": False, "intimate": False, "touristy": False, "hipster": False, "divey": False, "classy": False, "trendy": False, "upscale": False, "casual": True}, "Waiter Service": True, "Accepts Credit Cards": True, "Good for Kids": True, "Good For Groups": True, "Price Range": 1}, "type": "business"},
      {"business_id": "LRKJF43s9-3jG9Lgx4zODg", "full_address": "4910 County Rd V\nDe Forest, WI 53532", "hours": {"Monday": {"close": "22:00", "open": "10:30"}, "Tuesday": {"close": "22:00", "open": "10:30"}, "Friday": {"close": "22:00", "open": "10:30"}, "Wednesday": {"close": "22:00", "open": "10:30"}, "Thursday": {"close": "22:00", "open": "10:30"}, "Sunday": {"close": "22:00", "open": "10:30"}, "Saturday": {"close": "22:00", "open": "10:30"}}, "open": True, "categories": ["Food", "Ice Cream & Frozen Yogurt", "Fast Food", "Restaurants"], "city": "De Forest", "review_count": 7, "name": "Culver's", "neighborhoods": [], "longitude": -89.374983, "state": "WI", "stars": 4.5, "latitude": 43.251044999999998, "attributes": {"Take-out": True, "Wi-Fi": "free", "Takes Reservations": False, "Delivery": False, "Parking": {"garage": False, "street": False, "validated": False, "lot": True, "valet": False}, "Wheelchair Accessible": True, "Attire": "casual", "Accepts Credit Cards": True, "Good For Groups": True, "Price Range": 1}, "type": "business"},
      {"business_id": "RgDg-k9S5YD_BaxMckifkg", "full_address": "631 S Main St\nDe Forest, WI 53532", "hours": {"Monday": {"close": "22:00", "open": "11:00"}, "Tuesday": {"close": "22:00", "open": "11:00"}, "Friday": {"close": "22:30", "open": "11:00"}, "Wednesday": {"close": "22:00", "open": "11:00"}, "Thursday": {"close": "22:00", "open": "11:00"}, "Sunday": {"close": "21:00", "open": "16:00"}, "Saturday": {"close": "22:30", "open": "11:00"}}, "open": True, "categories": ["Chinese", "Restaurants"], "city": "De Forest", "review_count": 3, "name": "Chang Jiang Chinese Kitchen", "neighborhoods": [], "longitude": -89.343721700000003, "state": "WI", "stars": 4.0, "latitude": 43.2408748, "attributes": {"Take-out": True, "Has TV": False, "Outdoor Seating": False, "Attire": "casual"}, "type": "business"}
    ]


@QuestionList.add
class CityModel(MLValidateMixin):
  """
  The venues belong to different cities.  You can image that the ratings in some cities are probably higher than others and use this as an estimator.

  **Note:** `def solution` takes an argument `record`.  Samples of `record` are given in `_test_json`.

  **Exercise**: Build an estimator that uses `groupby` and `mean` to compute the average rating in that city.  Use this as a predictor.
  """
  _fields = ['city']

  @list_or_dict
  def solution(self, record):
    return 0.


@QuestionList.add
class LatLongModel(MLValidateMixin):
  """
  You can imagine that a city-based model might not be sufficiently fine-grained.  For example, we know that some neighborhoods are trendier than others.  We might consider a K Nearest Neighbors or Random Forest based on the latitude longitude as a way to understand neighborhood dynamics.

  **Exercise**: You should implement a generic `ColumnSelectTransformer` that is passed which columns to select in the transformer and use a non-linear model like `neighbors.KNeighborsRegressor` ([docs](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html)) or `ensemble.RandomForestRegressor` ([docs](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)) as the estimator (why would you choose a non-linear model?).  Bonus points if you wrap the estimator in `grid_search.GridSearchCV` and use cross-validation to determine the optimal value of the parameters.
  """
  _fields = ['longitude', 'latitude']

  @list_or_dict
  def solution(self, record):
    return 0.


@QuestionList.add
class CategoryModel(MLValidateMixin):
  """
  Venues have categories with varying degrees of specificity, e.g.
  ```python
  [Doctors, Health & Medical]
  [Restaurants]
  [American (Traditional), Restaurants]
  ```
  With a large sparse feature set like this, we often use a cross-validated regularized linear model.
  **Exercise:**

  1. Build a custom transformer that massages the data so that it can be fed into `feature_extraction.DictVectorizer` ([docs](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html)), which in turn generates a large matrix gotten by One-Hot-Encoding.  Feed this into a Linear Regression (and cross validate it!).  Can you beat this with another type of non-linear estimator?

  1. Some categoreis (e.g. Restaurants) are not very speicifc.  Others (Japanese sushi) are much more so.  How can we account for this in our model (*Hint:* look at TF-IDF).
  """
  _fields = ['categories']

  @list_or_dict
  def solution(self, record):
    return 0.


@QuestionList.add
class AttributeKnnModel(MLValidateMixin):
  """
  Venues have (potentially nested) attributes.  For example,
  ``` python
  { 'Attire': 'casual',
    'Accepts Credit Cards': True,
    'Ambience': {'casual': False, 'classy': False }}
  ```
  Categorical data like this should often be transformed by a One Hot Encoding.  For example, we might flatten the above into something like this:
  ``` python
  { 'Attire_casual' : 1,
    'Accepts Credit Cards': 1,
    'Ambience_casual': 0,
    'Ambience_classy': 0 }
  ```
  **Exercise:** Build a custom transformer that flattens attributes and feed this into `DictVectorizer`.  Feed it into a (cross-validated) linear model (or something else!)
  """
  _fields = ['attributes']

  @list_or_dict
  def solution(self, record):
    return 0.


@QuestionList.add
class FullModel(MLValidateMixin):
  """
  So far we have only built models based on individual features.  We could obviously combine them.  One (highly recommended) way to do this is through a [feature union](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.FeatureUnion.html).

  **Exercise:** Combine all the above models using a feature union.  Notice that a feature union takes transformers, not models as arguements.  The way around this is to build a transformer

  ```class ModelTransformer```

  that outputs the prediction in the transform method, thus turning the model into a transformer.  Use a cross-validated linear regression (or some other algorithm) to weight these signals.
  """
  _fields = None

  @list_or_dict
  def solution(self, record):
    return 0.

