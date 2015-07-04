"""
word_count.py
"""

from mrjob.job import MRJob
#from mrjob.compat import get_jobconf_value


class MRWordFrequencyCount(MRJob):
    """
    """

    def mapper(self, _, line):
        """
        Performs sorting for map-reduce \n
        Returns: a (k1,v1) tuple (i.e. <'cars', 1>) for each unit of the input
        
        Parameters
        ------
        line: string, a line of text terminated by '\n'
        """
        
        line = line.lower() 
        yield "chars", len(line)
        yield "words", len(line.split())
        yield "lines", 1
        
        
    def reducer(self, key, values):
        """
        Combines the unigram counts (all tuples sharing a key) \n
        Returns: a  (k1, v2) tuple (i.e. <'cars', 34>
        
        Parameters
        ------
        key: string, a word returned from the mapper
        value: int, a list of all counts of the key
        """
        yield key, sum(values)  # yep, 1 line

    
## Execution Code ###
if __name__ == '__main__':
    MRWordFrequencyCount.run()
