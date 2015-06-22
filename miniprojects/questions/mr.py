"""
We are going to be running mapreduce jobs on the wikipedia dataset.  The dataset is available (pre-chunked) on [s3](s3://thedataincubator-course/mrdata/simple/).

To solve this, you will need to run mrjob on AWS EMR.  The data is stored on S3.  For development, we highly recommend you download a single chunk onto your computer:
```
wget https://s3.amazonaws.com/thedataincubator/coursedata/mrdata/simple/part-00006.xml.bz2
```
Then take a small sample that is small enough that mrjob can process the it in a few seconds.  Your development cycle should be:

  1. Get your job to work locally on the sampled chunk.  This will greatly speed-up your development.

  2. Get your job to work localy on the full chunk you downloaded.

  ** Assignment **: for your own edification, run the wordcount mapreduce without combiner and run one with a combiner to observe the performance benefit.  You can use the [unix time utility](http://en.wikipedia.org/wiki/Unix_time) to measure this more precisely.

  3. Get your job to work on EMR for all of simple english.

  4. Get your job to work on EMR for all of english wikipedia.

By default, mrjob (when run on EMR) only uploads the mrjob python file and no supporting libraries.

  1. You can always import members of the standard library as they come with any python distribution

  2. If you wish to use non-standard libraries, you will have to follow the [instructions to `pip install` them onto the boxes](http://mrjob.readthedocs.org/en/latest/guides/setup-cookbook.html).

  3. If you wish to include code from other local python files, use [tar them up](https://pythonhosted.org/mrjob/guides/setup-cookbook.html#running-a-makefile-inside-your-source-dir)) to upload them to EMR.

  4. EMR runs python 2.6 but Digital Ocean has python 2.7 installed.  The [lxml](https://pypi.python.org/pypi/lxml/2.3) library changes between these two python versions.  You may wish to start using [virtualenv](https://virtualenv.pypa.io/en/latest/) to simulate python2.6 on Digital Ocean.

Finally, if you want to structure your mrjob code well, you will want to have multiple mrjobs in a single module.  As a matter of good style, we recommended that you write each separate mapreduce as it's own class.  Then write a wrapper module that defines the logic for combining steps.  You can combine multiple steps by overriding the [steps method](https://pythonhosted.org/mrjob/guides/writing-mrjobs.html#multi-step-jobs).

Here are some helpful articles on how mrjob works and how to pass parameters to your script:
  - [How mrjob is run](https://pythonhosted.org/mrjob/guides/concepts.html#how-your-program-is-run)
  - [Adding passthrough options](https://pythonhosted.org/mrjob/job.html#mrjob.job.MRJob.add_passthrough_option)
  - [An example of someone solving similar problems](http://arunxjacob.blogspot.com/2013/11/hadoop-streaming-with-mrjob.html)

"""

from lib import QuestionList, Question, StringNumberListValidateMixin, JsonValidateMixin, TupleListValidateMixin
QuestionList.set_name("mr")

class TupleNumberListValidateMixin(TupleListValidateMixin):
  @classmethod
  def list_length(cls):
    return 100

  @classmethod
  def tuple_validators(cls):
    return (cls.validate_tuple, cls.validate_number)

@QuestionList.add
class Top100WordsSimpleWikipediaPlain(StringNumberListValidateMixin, Question):
  """
  Return a list of the top 100 words in article text (in no particular order).

  You will need to write this as two map reduces:

  1. The first job is similar to standard wordcount but with a few .  The data provided for wikipedia is in in *.xml.bz2 format.  Mrjob will automatically decompress bz2.  We'll deal with the xml in the next question.  For now, just treat it as text.  A few Hints:

    1. To split the words, use the regular expression "\w+".

    2. Words are not case sensitive: i.e. "The" and "the" reference to the same word.  You can use `string.lower()` to get a single case-insenstive canonical version of the data.

  2. The second job will take a collection of pairs `(word, count)` and filter for only the highest 100.  A few notes:

    1. To make the job more reusable make the job find the largest `n` words where `n` is a parameter obtained via [`get_jobconf_value`](https://pythonhosted.org/mrjob/utils-compat.html).

    2. We have to keep track of at most the `n` most popular words.  As long as `n` is small, e.g. 100, we can keep track of the *running largest n* in memory.  Use a [Heap](http://en.wikipedia.org/wiki/Heap_(data_structure)) [Priority Queue](http://en.wikipedia.org/wiki/Priority_queue) structure for this.  It is implemented in python as [heapq](https://docs.python.org/2/library/heapq.html), which is conveniently part of the standard library.  You may be asked about this data structure on an interview so it is good to get practice with it now.

    3. To obtain the largest `n`, we need to first obtain the largest n elements per chunk from the mapper, output them to the same key (reducer), and then collect the largest n elements of those in the reducer (**Question:** why does this gaurantee that we have found the largest n over the entire set?)  Given that we are using a priority queue, we will need to first initialize it, then add it for each record, and then output the top `n` after seeing each record.  For mappers, notice that these three phases correspond nicely to these three functions:

      - `mapper_init`
      - `mapper`
      - `mapper_final`

      There are similar functions in the reducer.  Also, while the run method to launch the mapreduce job is a classmethod:

      ```
      if __name__ == '__main__':
        MRWordCount.run()
      ```

      actual objects are instantiated on the map and reduce nodes.  More precisely, a separate mapper class is instantiated in each map node and a reducer class is instantiated in each reducer node.  This means that the three mapper functions can pass state through `self`, e.g. `self.heap`.  Remember that to pass state between the map and reduce phase, you will have to use `yield` in the mapper and read each line in the reducer.

    3. When you have the top 100 words and their count, simply download the results (using aws cli) and copy and paste the results below:
  """

  def solution(self):
    """
    A list of 100 tuples of word and count: e.g.
    ```
    [('the', 39583), ('a', 395739), .... ]
    ```
    """
    return [("the", 1596419)] * 100


@QuestionList.add
class Top100WordsSimpleWikipediaText(StringNumberListValidateMixin, Question):
  """
  Notice that the words `page` and `text` make it into the top 100 words in the prevous problem.  These are not common English words!  If you look at the xml formatting, you'll realize that these are xml tags.  You should parse the files so that tags like `<page></page>` should not be included in your total, nor should words outside of the tag `<text></text>`.  **Hints**:

    1. Notice that [xml](https://docs.python.org/2/library/xml.etree.elementtree.html) will parse a string as xml and is part of the standard library.

    2. In order to parse the text, we will have to accumulate a `<page></page>` worth of data and then parse the resulting wikipedia format string.
  """

  def solution(self):
    """
    A list of 100 tuples of word and count using the same format.
    """
    return [("the", 1579644)] * 100


@QuestionList.add
class Top100WordsSimpleWikipediaNoMetaData(StringNumberListValidateMixin, Question):
  """
  Finally, notice that 'www' and 'http' make it into the list of top 100 words in the previous problem.  These are also not common English words!  These are clearly the url in hyperlinks.  Looking at the format of [Wikipedia links](http://en.wikipedia.org/wiki/Help:Wiki_markup#Links_and_URLs) and [citations](http://en.wikipedia.org/wiki/Help:Wiki_markup#References_and_citing_sources), you'll notice that they tend to appear within single and double brackets and curly braces.  *Hint*:

    1. This is a great place to use class inheritance so you can reuse the functionality of the previous class.

    2. You can either write a simple parser to eliminate the text within brackets, angle braces, and curly braces or you can use a package like the colorfully-named [mwparserfromhell](https://github.com/earwig/mwparserfromhell/), which has been provisioned on the machines already.
  """

  def solution(self):
    """
    A list of 100 tuples of word and count using the same format.
    """
    return [("the", 1561900)] * 100


class StatsJsonValidateMixin(JsonValidateMixin):
  _keys = ["count", "mean", "stdev", "5%", "25%", "median", "75%", "95%"]

  @classmethod
  def keys(cls):
    return cls._keys


@QuestionList.add
class LinkStatsSimpleWikipedia(StatsJsonValidateMixin, Question):
  """
  Compute link statistics for Simple Wikipedia.  Let's look at some summary statistics on the number of unique links on a page to other wikipedia articles.  Return the number of articles (count), average number of links, standard deviation, and the 5%, 25%, median, 75%, and 95% quantiles.

  1. Notice that the library `mwparserfromhell` has classes that support the method `filter_wikilinks`.

  2. You will need to compute these statistics in a way that requires O(1) memory.  You should be able to compute the first few (i.e. non-quantile) statistics exactly by looking at the first few moments of a distribution.  The quantile quantities can be accurately estimated by using reservoir sampling with a large reservoir.

  3. If there are multiple links to the article have it only count for 1.  This keeps our results from becoming too skewed.
  """
  def solution(self):
    """
    Return this json object
    """
    return {
      "count": 0.,
      "mean": 0.,
      "stdev": 0.,
      "5%": 0.,
      "25%": 0.,
      "median": 0.,
      "75%": 0.,
      "95%": 0.,
    }


@QuestionList.add
class LinkStatsEnglishWikipedia(StatsJsonValidateMixin, Question):
  """
  The same thing but for all of English Wikipedia.  This is the real test of how well your algorithm scales!
  """
  def solution(self):
    """
    Return this json object
    """
    return {
      "count": 0.,
      "mean": 0.,
      "stdev": 0.,
      "5%": 0.,
      "25%": 0.,
      "median": 0.,
      "75%": 0.,
      "95%": 0.,
    }


@QuestionList.add
class Top100DoubleLinkSimpleWikipedia(TupleNumberListValidateMixin, Question):
  """
  Instead of analyzing single links, let's look at double links.  That is, pages A and C that are connected through many pages B where there is a link
  `A -> B -> C`
  Find the list of all pairs `(A, C)` that have the 100 "most" connections (see below for the definition of "most").  This should give us a notion that the articles `A` and `C` refer to tightly related concepts.

  1. This is essentially a Matrix Multiplication problem.  If the adjacency matrix is denoted $M$ (where $M_{ij}$ represents the link between $i$ an $j$), we are looking for the highest 100 elements of the matrix $M M$.

  2. Notice that a lot of Category pages (denoted "Category:.*") have a high link count and will rank very highly according to this metric.  Wikipedia also has `Talk:` pages, `Help:` pages, and static resource `Files:`.  All such "non-content" pages (and there might be more than just this) and links to them should be first filtered out in this analysis.

  3. Some pages have more links than others.  If we just counted the number of double links between pages, we will end up seeing a list of articles with many links, rather than concepts that are tightly connected.

    a. One strategy is to weight each link as
      $\frac{1}{n}$
      where $n$ is the number links on the page.  This way, an article has to spread it's "influence" over all $n$ of its links.  However, this can throw off the results if $n$ is small.

    b. Instead, try weighting each link as
      $\frac{1}{n+10}$
      where 10 sets the "scale" in terms of number of links above which a page becomes "significant".  The number 10 was somewhat arbitrarily chosen but seems to give reasonably relevant results.

  4. Again, if there are multiple links from a page to another, have it only count for 1.  This keeps our results from becoming skewed by a single page that references the same page multiple times.

  Don't be afraid if these answers are not particularly insightful.  Simplewikipedia is not as rich as Englishwikipedia.  However, you should notice that the articles are closely related conceptually.
  """
  def solution(self):
    """
    Return this json object
    """
    return [(("Nord-Pas-de-Calais", "Pas-de-Calais"), 2.269110852005026)] * 100

