"""
word_count_multistep

Multi-Step Jobs:
    
    To define multiple steps, override `MRJob::steps()` to return 
    a list of `mr()` calls
    
    http://pythonhosted.org/mrjob/guides/writing-mrjobs.html
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from itertools import islice
import re


class MRMostUsedWord(MRJob):
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
        'counts' is moved to tpl[0] so we can easily use python::max()
        """
        yield None, (sum(counts), word)  # This 'None' initializes the next 
                                         # reducer, so that when the first tpl
                                         # is sent, reducer_find_max exists to 
                                         # receive it.
        
    
    def reducer_find_max_word(self, _, word_count_pairs):
        """
        'word_count_pairs' is list/gen of (count, word) ~ (key, value)
        That tuple is the output of yield...
        """
        yield max(word_count_pairs)
        

    def reducer_top_100_words(self, _, word_count_pairs):
        """
        Returns the 100 most frequent words as (count, word)
        """
        word_count_pairs = sorted(word_count_pairs, reverse=True)[0:100]
        # print "Size", len(word_count_pairs)  # @debug
        
        for tpl in word_count_pairs:
            yield tpl
            

    def steps(self):
        """
        Override MRJob::steps() to enable two-step job.
        Define the job as two steps.
        (Step1: MCR, Step2:R - chain reducers this way)
        """
        return [
            MRStep(mapper = self.mapper_get_words,
                   combiner = self.combiner_count_words,
                   reducer = self.reducer_count_words),
            MRStep(reducer = self.reducer_top_100_words),
            #MRStep(reducer = self.reducer_find_max_word) # can't do 3 reducers for some reason
        ]

    
## Execution Code ###
if __name__ == '__main__':
    MRMostUsedWord.run()
