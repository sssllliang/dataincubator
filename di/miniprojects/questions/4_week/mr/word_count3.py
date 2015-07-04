"""
word_count3.py


    Single-step jobs

    The simplest way to write a one-step job is to subclass 
    MRJob and override a few methods: mapper(), combiner(), reducer().
    
    Can also override *_init(), *_final(), *_cmd(), *_pre_filter().

    http://pythonhosted.org/mrjob/guides/writing-mrjobs.html
"""

from mrjob.job import MRJob
#from mrjob.compat import get_jobconf_value
import re


class MRWordFreqCount(MRJob):
    """
    """

    global WORD_RE                  # if this is in mapper, it will be      
    WORD_RE = re.compile(r'[\w]+')  #  called millions of times


    def mapper(self, _, line):
        """
        """
        for word in WORD_RE.findall(line):
            yield word.lower(), 1  # returns a generator of tuples: (word, 1)
        

    def combiner(self, word, counts):  # (key,value)
        """
        """
        yield word, sum(counts)


    def reducer(self, word, counts):
        """
        """
        yield word, sum(counts)  # yup, 1 line

    
## Execution Code ###
if __name__ == '__main__':
    MRWordFreqCount.run()
