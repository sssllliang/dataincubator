from lib import QuestionList, Question, StringNumberListValidateMixin, \
TupleListValidateMixin, catch_validate_exception

QuestionList.set_name("spark_pagerank")

"""
# The PageRank Algorithm

In this assignment, you'll run PageRank on a list of connected citations in High Energy
Physics. The PageRank algorithm assigns a measure of importance (a "rank") to each document 
in a set based on how many documents have links to it. 

Download the dataset of citations with
`s3cmd get s3://thedataincubator-course/spark_pagerank/Cit-HepPh.txt`
Here's the original source and description: http://snap.stanford.edu/data/ca-AstroPh.html

## Implementation: some hints

There are two important RDDs you should be making:
	1. (pageID, linkList) : the list of neighbors for each page
	2. (pageID, rank) : contains the current rank for each page

A page's rank is a sum of "contributions" from each of its neighbors, which is its neighbor's 
rank divided by the neighbor's number of neighbors. To calculate, passes over the 
set of page ranks and update ranks during each pass until the ranks converge. 

Algorithm steps:
	1. Initialize each page's rank to 1.0.
	2. On each iteration, have page p send a contribution of rank(p) / numNeighbors(p) to its 
	neighbors (i.e. the pages it has links to).
	3. Set each page's rank to 0.15 + 0.85 * contributionsReceived. The last two steps repeat 
	for several iterations, during which the algorithm will converge to the correct P

## Spark Procedural hints
1. Write a function to filter out the header lines in the data.
2. Write a "main" function that reads in the text file, filters the header lines, 
splits each line into a key and value, does a distinct group by on each key (source node), 
then completes enough iterations of PageRank for the ranks to converge.
3. Write the top 100 ranks to file in the format: {node}\t{rank}

# Submission Instructions
As with the NY Social Diary pagerank miniproject, your task is to get the ranks of the 
highest 100-ranking nodes and to return a list of tuples with the node id as a String
and the rank as a float (see below).

Since we'd like you to implement in Scala, we will only be checking the results and 
not code (as the grading app doesn't support Scala grading right now)
"""

@QuestionList.add
class TopHundredNodes(StringNumberListValidateMixin, Question):
	"""
	Return a list of (String, float) tuples of the form
	`("node_id", rank)`
	that are the top 100 nodes, ordered by ** node id ** descending
	Hint: the first (top) node should be 9912552
	"""
	def solution(self):
		return [('9912552',0.2671914219791478)] * 100
