from lib import (QuestionList, Question, MovieMixin, _number_validate,
  catch_validate_exception)

QuestionList.set_name("cf")

class MovieReviewsValidateMixin(MovieMixin, Question):
  @classmethod
  def _test_records(cls):
    return [
      "1::122::5::838985046",
      "1::185::5::838983525",
      "2::736::3::868244698",
      "2::780::3::868244698",
      "3::590::3.5::1136075494",
    ]

  @catch_validate_exception
  def validate(self):
    # check that this
    for case in self.get_test_cases():
      solutions = self.solution(*case['args'], **case['kwargs'])
      for sol in solutions:
        val = _number_validate(sol)

        if val is not None:
          return val

    return None


@QuestionList.add
class BaselineModel(MovieReviewsValidateMixin):
  @list_or_dict
  def solution(self, record):
    return 0.


@QuestionList.add
class TemporalModel(MovieReviewsValidateMixin):
  @list_or_dict
  def solution(self, record):
    return 0.


@QuestionList.add
class MatrixFactorizationModel(MovieReviewsValidateMixin):
  @list_or_dict
  def solution(self, record):
    return 0.
