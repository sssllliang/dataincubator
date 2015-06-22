"""
Time series prediction presents its own challenges which are different from machine-learning problems.  Like many other classes of problems, it also presents a number of special features which are common.

## Fetch the data:
http://s3.amazonaws.com/thedataincubator/coursedata/mldata/train.txt.gz

The columns of the data correspond to the
  - year
  - month
  - day
  - hour
  - temp
  - dew_temp
  - pressure
  - wind_angle
  - wind_speed
  - sky_code
  - rain_hour
  - rain_6hour
  - city

We will focus on using the temporal elements to predict the temperature.

## Cross-validation is Different

1. Cross validation is very different for time series than with other machine-learning problem classes.  In normal machine learning, we select a random subset of data as a validation set to estimate performance.  In time series, we have to consider the problem that we are trying to solve is often to predict a value in the future.  Therefore, the validation data always has to occur *after* the training data.  As a simple example, consider that it would not be very useful to have a predictor of tomorrow's temperature that depended on the temperature the day after.<br/>
We usually handle this by doing a **sliding-window validation method**.  That is, we train on the last $n$ data points and validate the prediction on the next $m$ data points, sliding the $n + m$ training / validation window in time.  In this way, we can estimate the parameters of our model.  To test the validity of the model, we might use a block of data at the end of our time series which is reserved for testing the model with the learned parameters.

1. Another concern is wheather the time series results are predictive.  In economics and finance, we refer to this as the ergodicity assumption, that past behavior can inform future behavior.  Many wonder if past behavoir in daily stock returns gives much predictive power for future behavior.

**Warning**: Feature generation is sometimes a little different for time-series.  Usually, feature generaiton on a set is only based on data in that training example (e.g. extracting the time of day of the temperature measurement).  In timeseries, we often want to use *lagged* data (the temperature an hour ago).  The easiest way to do this is to do the feature generation *before* making the training and validation split.

## Per city model:

It makes sense for each city to have it's own model.  Build a "groupby" estimator that takes an estimator as an argument and builds the resulting "groupby" estimator on each city.  That is, `fit` should fit a model per city while the `predict` method should look up the corresponding model and perform a predict on each, etc ...
"""

from numbers import Number
from lib import QuestionList, Question, list_or_dict, catch_validate_exception
QuestionList.set_name("ts")


class TimeSeriesRecordMixin(object):
  @classmethod
  def _test_txt(cls):
    return [
      "2000 01 01 00   -11   -72 10197   220    26     4     0     0 bos",
      "2000 01 01 01    -6   -78 10206   230    26     2     0 -9999 bos",
      "2000 01 01 02   -17   -78 10211   230    36     0     0 -9999 bos",
      "2000 01 01 03   -17   -78 10214   230    36     0     0 -9999 bos",
      "2000 01 01 04   -17   -78 10216   230    36     0     0 -9999 bos",
    ]

  @classmethod
  def get_test_cases(cls):
    return [{ 'args': [cls.get_records()], 'kwargs': {} }]

  @catch_validate_exception
  def validate(self):
    lst = self.solution(self._test_txt())
    if not isinstance(lst, (tuple, list)):
      return "Expected list, got %.200s." % str(lst)

    if len(lst) != 5:
      return "Expected list of length 5, got %.200s." % str(lst)

    for e in lst:
      if type(e) not in (float, int):
        return "Expected every element to be a tuple, got %.200s." % str(e)

@QuestionList.add
class MonthHourModel(TimeSeriesRecordMixin, Question):
  """
  ### Seasonality:
  There are two ways to handle seasonality.  Seasonality features are nice because they are good at projecting arbitrarily far into the future.

  The simplest (and perhaps most robust) is to have a set of indicator variables for each month.  **Question**: should month be a continuous or categorical variable?
  """
  @list_or_dict
  def solution(self, txt):
    return 0.


@QuestionList.add
class FourierModel(TimeSeriesRecordMixin, Question):
  """
  Since we know that temperature is roughly sinusoidal, we know that a reasonable model might be
  $$ y_t = k \sin\left( \frac{t - t_0}{T} \right) + \epsilon $$
  where $k$ and $t_0$ are parameters to be learned and $T$ is one year for seasonal variation.  While this is linear in $k$, it is not linear in $t_0$.  However, we know from Fourier analysis, that the above is equivalent to
  $$ y_t = A \sin\left( \frac{t}{T} \right) + B \cos\left( \frac{t}{T} \right) + \epsilon $$
  which is linear in $A$ and $B$.  This can be solved using a linear regression.
  """
  @list_or_dict
  def solution(self, txt):
    return 0.

