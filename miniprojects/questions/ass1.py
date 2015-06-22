from numbers import Number

from lib import QuestionList, Question, catch_validate_exception
QuestionList.set_name('ass1')

@QuestionList.add
class APlusB(Question):
  """
  What is a plus b?
  """
  def solution(self, a, b):
    return a+b


  """
  Do not touch!
  """
  @catch_validate_exception
  def validate(self):
    ans = self.solution(2, 3)
    if not isinstance(ans, Number):
      return "Answer is not a number! Need to return a single number."

    return None
