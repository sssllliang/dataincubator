"""
mr-Q1.py

Get top 100 words by counts

Multi-Step Jobs:
    
    To define multiple steps, override `MRJob::steps()` to return 
    a list of `mr()` calls
    
    Ref:
    http://pythonhosted.org/mrjob/guides/writing-mrjobs.html
  --------------------------------------------------------------------------
    
    Run Via Terminal Command:
    $ python mr-Q1.py data/part-00006.xml > results.txt
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import re


class MRTop100Words(MRJob):
    """
    """
    
    global WORD_RE                  # if this is in mapper, it will be      
    WORD_RE = re.compile(r'[\w]+')  # called millions of times

    def mapper_get_words(self, _, line):
        """
        Yield each word in the line
        """
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)  # returns a generator of tuples: (word, 1)
        

    def combiner_count_words(self, word, counts):  # (key,value)
        """
        Sum the words we've seen so far
        """
        yield (word, sum(counts))


    def reducer_count_words(self, word, counts):
        """
        Send all (counts, word) pairs to this reducer.
        """
        yield None, (word, sum(counts))  # This 'None' initializes the next 
                                         # reducer, so that when the first tpl
                                         # is sent, reducer_find_max exists to 
                                         # receive it.
    
    def get_key(self, tpl):
        """
        Keying function allowing word pair tuples to be sorted
        by second element ex:('the', 31) sorts as 31
        """
        return tpl[1]
    

    def reducer_top_100_words(self, _, word_count_pairs):
        """
        Returns the 100 most frequent words as (count, word)
        """
        word_count_pairs = sorted(word_count_pairs, key=self.get_key, reverse=True)
        word_count_pairs = word_count_pairs[0:100]
        #print "Size", len(word_count_pairs)  # @debug
            
        lst_top_100 = []
        for tpl in word_count_pairs:
            lst_top_100.append(tuple(tpl))
        
        print lst_top_100  # use `print` to preserve the list[tuple,...,tuple] format
        return

    def steps(self):
        """
        Override MRJob::steps() to enable a two-step job.
        Define the job as two steps.
        (Step1: MCR, Step2:R - chain reducers this way)
        """
        return [
            MRStep(mapper = self.mapper_get_words,
                   combiner = self.combiner_count_words,
                   reducer = self.reducer_count_words),
            MRStep(reducer = self.reducer_top_100_words),
        ]

    
## Execution Code ###
if __name__ == '__main__':
    MRTop100Words.run()
