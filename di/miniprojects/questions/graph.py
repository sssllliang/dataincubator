# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
[New York Social Diary](http://www.newyorksocialdiary.com/) provides a fascinating lens onto New York's socially well-to-do.  The data forms a natural social graph for New York's social elite.  Take a look at this page of a recent run-of-the-mill holiday party:

`http://www.newyorksocialdiary.com/party-pictures/2014/holiday-dinners-and-doers`

Besides the brand-name celebrities, you will notice the photos have carefully annotated captions labeling those that appear in the photos.  We can think of this as implicitly implying a social graph: there is a connection between two individuals if they appear in a picture together.

The first step is to fetch the data.  This comes in two phases.

The first step is to crawl the data.  We want photos from parties before December 1st, 2014.  Go to
`http://www.newyorksocialdiary.com/party-pictures`
to see a list of (party) pages.  For each party's page, grab all the captions.  *Hints*:

  1. Click on the on the index page and see how they change the url.  Use this to determine a strategy to get all the data.

  2. Notice that each party has a date on the index page.  Use python's `datetime.strptime` function to parse it.

  3. Some captions are not useful: they contain long narrative texts that explain the event.  Usually in two stage processes like this, it is better to keep more data in the first stage and then filter it out in the second stage.  This makes your work more reproducible.  It's usually faster to download more data than you need now than to have to redownload more data later.

Now that you have a list of all captions, you should probably save the data on disk so that you can quickly retrieve it.  Now comes the parsing part.

  1. Some captions are not useful: they contain long narrative texts that explain the event.  Try to find some heuristic rules to separate captions that are a list of names from those that are not.  A few heuristics include:
      - look for sentences (which have verbs) and as opposed to lists of nouns.  For example, [nltk does part of speech tagging](http://www.nltk.org/book/ch05.html) but it is a little slow.  There may also be heuristics that accomplish the same thing.
      - Look for commonly repeated threads (e.g. you might end up picking up the photo credtis).
      - Long captions are often not lists of people.  The cutoff is subjective so to be definitive, *let's set that cutoff at 250 characters*.

  2. You will want to separate the captions based on various forms of punctuation.  Try using `re.split`, which is more sophisticated than `string.split`.

  3. You might find a person named "ra Lebenthal".  There is no one by this name.  Can anyone spot what's happening here?

  4. This site is pretty formal and likes to say things like "Mayor Michael Bloomberg" after his election but "Michael Bloomberg" before his election.  Can you find other ('optional') titles that are being used?  They should probably be filtered out b/c they ultimately refer to the same person: "Michael Bloomberg."

For the analysis, we think of the problem in terms of a [network](http://en.wikipedia.org/wiki/Computer_network) or a [graph](http://en.wikipedia.org/wiki/Graph_%28mathematics%29).  Any time a pair of people appear in a photo together, that is considered a link.  What we have described is more appropriately called an (undirected) [multigraph](http://en.wikipedia.org/wiki/Multigraph) with no self-loops but this has an obvious analog in terms of an undirected [weighted graph](http://en.wikipedia.org/wiki/Graph_%28mathematics%29#Weighted_graph).  In this problem, we will analyze the social graph of the new york social elite.

For this problem, we recommend using python's `networkx` library.
"""

from lib import QuestionList, Question, StringNumberListValidateMixin, TupleListValidateMixin
QuestionList.set_name("graph")

@QuestionList.add
class Degree(StringNumberListValidateMixin, Question):
  """
  The simplest question you might want to ask is 'who is the most popular'?  The easiest way to answer this question is to look at how many connections everyone has.  Return the top 100 people and their degree.  Remember that if an edge of the graph has weight 2, it counts for 2 in the degree.
  """
  def solution(self):
    """
    A list of 100 tuples of (name, degree) in descending order of degree
    """
    #return [('Alec Baldwin', 69)] * 100
    return [(u'Jean Shafiroff', 452), (u'Mark Gilbertson', 372), (u'Gillian Miniter', 345), (u'Alexandra Lebenthal', 279), (u'Geoffrey Bradfield', 262), (u'Somers Farkas', 215), (u'Andrew Saffir', 205), (u'Debbie Bancroft', 202), (u'Yaz Hernandez', 198), (u'Kamie Lightburn', 198), (u'Alina Cho', 196), (u'Eleanora Kennedy', 191), (u'Jamee Gregory', 188), (u'Sharon Bush', 187), (u'Muffie Potter Aston', 170), (u'Allison Aston', 168), (u'Mario Buatta', 166), (u'Lucia Hwong Gordon', 162), (u'Lydia Fenet', 160), (u'Bonnie Comley', 160), (u'Karen LeFrak', 157), (u'Patrick McMullan', 154), (u'Deborah Norville', 153), (u'John', 152), (u'Bettina Zilkha', 147), (u'Barbara Tober', 139), (u'Michael Bloomberg', 139), (u'Martha Stewart', 138), (u'Audrey Gruss', 136), (u'Stewart Lane', 136), (u'Liz Peek', 134), (u'Grace Meigher', 128), (u'Diana Taylor', 126), (u'Daniel Benedict', 126), (u'Kipton Cronkite', 126), (u'Roric Tobin', 125), (u'Nicole Miller', 125), (u'Rosanna Scotto', 124), (u'Margo Langenberg', 121), (u'Fe Fendi', 121), (u'Martha Glass', 120), (u'Janna Bullock', 120), (u'Adelina Wong Ettelson', 119), (u'Barbara Regna', 119), (u'Elizabeth Stribling', 118), (u'Leonard Lauder', 118), (u'Couri Hay', 118), (u'Margaret Russell', 117), (u'Alexandra Lind Rose', 117), (u'Lisa Anastos', 116), (u'Jennifer Creel', 116), (u'Dennis Basso', 115), (u'Julia Koch', 114), (u'Amy Fine Collins', 113), (u'Gregory Long', 113), (u'Sylvester Miniter', 112), (u'Wendy Carduner', 111), (u'Nathalie Kaplan', 108), (u'Deborah Roberts', 107), (u'Michele Herbert', 107), (u'Stephanie Winston Wolkoff', 105), (u'Dayssi Olarte de Kanavos', 105), (u'Gerald Loughlin', 105), (u'David', 105), (u'CeCe Black', 104), (u'Hilary Geary Ross', 104), (u'Karen Klopp', 104), (u'Fernanda Kellogg', 104), (u'Clare McKeon', 103), (u'Coco Kopelman', 103), (u'Alexia Hamm Ryan', 102), (u'Russell Simmons', 101), (u'Michael', 101), (u'Coralie Charriol Paul', 101), (u'Richard Johnson', 100), (u'Mary Davidson', 99), (u'Fern Mallis', 99), (u'Felicia Taylor', 99), (u'Alec Baldwin', 98), (u'Wilbur Ross', 98), (u'Frederick Anderson', 98), (u'Susan Shin', 98), (u'Amy Hoadley', 98), (u'Evelyn Lauder', 96), (u'Dawne Marie Grannum', 96), (u'Jonathan Tisch', 95), (u'Donna Karan', 94), (u'Melanie Holland', 93), (u'Suzanne Cochran', 92), (u'Pamela Fiori', 92), (u'Liliana Cavendish', 92), (u'Paula Zahn', 91), (u'Kelly Rutherford', 91), (u'Jonathan Farkas', 91), (u'Tory Burch', 91), (u'Georgina Schaeffer', 90), (u'Peter', 89), (u'Lizzie Tisch', 89), (u'Lauren Bush', 88), (u'Caryn Zucker', 88)]


@QuestionList.add
class PageRank(StringNumberListValidateMixin, Question):
  """
  A similar way to determine popularity is to look at their [pagerank](http://en.wikipedia.org/wiki/PageRank).  Pagerank is used for web ranking and was originally [patented](http://patft.uspto.gov/netacgi/nph-Parser?patentnumber=6285999) by Google and is essentially the [stationary distribution](http://en.wikipedia.org/wiki/Markov_chain#Stationary_distribution_relation_to_eigenvectors_and_simplices) of a [markov chain](http://en.wikipedia.org/wiki/Markov_chain) implied by the social graph.

  Use 0.85 as the damping parameter so that there is a 15% chance of jumping to another vertex at random.
  """
  def solution(self):
    """
    A list of 100 tuples of the form (name, pagerank) in descending order of pagerank
    """
    #return [('Martha Stewart', 0.0002051725372886844)] * 100
    return [(u'Jean Shafiroff', 0.0005831722985428765), (u'Mark Gilbertson', 0.0005029581752187725), (u'Gillian Miniter', 0.00043763371703257154), (u'Alexandra Lebenthal', 0.0003750824310072431), (u'Geoffrey Bradfield', 0.00034383419825139615), (u'Andrew Saffir', 0.0003406379343478819), (u'Somers Farkas', 0.0002918119204229116), (u'Debbie Bancroft', 0.0002843851396110316), (u'Sharon Bush', 0.0002758033395074356), (u'Kamie Lightburn', 0.0002747249673271048), (u'Mario Buatta', 0.00026948073538413244), (u'Yaz Hernandez', 0.00026047395963712004), (u'Lydia Fenet', 0.00025666340064083335), (u'Alina Cho', 0.0002501959393879638), (u'Patrick McMullan', 0.000243809426282124), (u'Eleanora Kennedy', 0.0002359904562926031), (u'Kipton Cronkite', 0.00022981956005412957), (u'Barbara Tober', 0.00022687708594512255), (u'Jamee Gregory', 0.0002257607829946866), (u'Lucia Hwong Gordon', 0.0002221343979923462), (u'Michael Bloomberg', 0.00020374957272388538), (u'Karen LeFrak', 0.0001996799011257205), (u'Allison Aston', 0.00019960549503321618), (u'Bonnie Comley', 0.00019905045908912963), (u'Martha Stewart', 0.0001990312448169071), (u'Bettina Zilkha', 0.00019678867357155589), (u'Leonard Lauder', 0.00019649256782314326), (u'Deborah Norville', 0.00019605716248278842), (u'Liz Peek', 0.0001896309242063033), (u'Janna Bullock', 0.00018784137818617024), (u'Fernanda Kellogg', 0.00018672561162604015), (u'Steven Stolman', 0.00018352573769431864), (u'Amy Fine Collins', 0.00018211702107748454), (u'Audrey Gruss', 0.00017789738018224164), (u'Muffie Potter Aston', 0.00017770758077044404), (u'Grace Meigher', 0.0001776024724942688), (u'Michele Herbert', 0.0001768591752199749), (u'Lisa Anastos', 0.00017382941689739423), (u'Daniel Benedict', 0.000172212513440389), (u'Dawne Marie Grannum', 0.0001722016785888504), (u'Diana Taylor', 0.00017207915734403527), (u'Michele Gerber Klein', 0.0001719088106294194), (u'Russell Simmons', 0.00017165192622182283), (u'Rosanna Scotto', 0.0001709907913335327), (u'Nicole Miller', 0.0001709162436484858), (u'Dennis Basso', 0.00016846857610027912), (u'Elizabeth Stribling', 0.00016769209105849456), (u'Adelina Wong Ettelson', 0.00016764726474373), (u'Susan Shin', 0.00016631601160450258), (u'Stewart Lane', 0.00016515301695425993), (u'Georgina Schaeffer', 0.00016497480578089936), (u'Jennifer Creel', 0.00016457686273929384), (u'Alexandra Lind Rose', 0.0001620483364639753), (u'Margo Langenberg', 0.00016087798709539357), (u'Nathalie Kaplan', 0.00015941724092850053), (u'Fern Mallis', 0.00015872673087943885), (u'Roric Tobin', 0.00015844188920641282), (u'Margaret Russell', 0.00015726806186581858), (u'Barbara Regna', 0.00015695162508931132), (u'Kristian Laliberte', 0.00015668105692882292), (u'Fe Fendi', 0.00015548902447149436), (u'Karen Klopp', 0.00015524186830238873), (u'Dayssi Olarte de Kanavos', 0.00015448101396137179), (u'Daniel Boulud', 0.00015288504371695406), (u'Richard Johnson', 0.0001518177173000829), (u'Gregory Long', 0.00015131959660142323), (u'Mary Davidson', 0.00014944128945577304), (u'Tinsley Mortimer', 0.00014914088996387646), (u'CeCe Black', 0.00014880595338458968), (u'Deborah Roberts', 0.00014863668182352332), (u'Melanie Holland', 0.00014648393954256225), (u'Donna Karan', 0.000146410540052822), (u'Herbert Pardes', 0.00014597308569009457), (u'Alec Baldwin', 0.00014567696338635495), (u'Pamela Fiori', 0.00014550606345762796), (u'Wendy Carduner', 0.00014533949628462188), (u'Martha Glass', 0.0001451815279851854), (u'Julia Koch', 0.00014226028844042048), (u'Evelyn Lauder', 0.00014155220144445964), (u'R. Couri Hay', 0.00014142906306502831), (u'Coralie Charriol Paul', 0.0001401188503617183), (u'Paula Zahn', 0.00013918655378051536), (u'Peter Lyden', 0.00013840167506220478), (u'Clare McKeon', 0.00013789443153521108), (u'Alexia Hamm Ryan', 0.00013773077572255482), (u'Diana DiMenna', 0.00013657641925503728), (u'Beth Rudin DeWoody', 0.00013604518105416003), (u'Coco Kopelman', 0.00013545152260894847), (u'Bette Midler', 0.00013497111228699365), (u'Hilary Geary Ross', 0.00013482231718518647), (u'Tina Brown', 0.00013316975768097301), (u'Felicia Taylor', 0.00013284542598346314), (u'Amy Phelan', 0.00013282364351139983), (u'Denise Rich', 0.00013267623358246265), (u'Kelly Rutherford', 0.00013205753341297223), (u'Bunny Williams', 0.00013118319999340657), (u'Museum Ellen V. Futter', 0.0001301754868576611), (u'Charlotte Moss', 0.00012988309165736496), (u'Amy Hoadley', 0.00012780663055938837), (u'Jill Zarin', 0.000127308667828596)]


@QuestionList.add
class BestFriends(TupleListValidateMixin, Question):
  """
  Another interesting question is who tend to co-occur with each other.  Give us the 100 edges with the highest weights

  Google these people and see what their connection is.  Can we use this to detect instances of infidelity?
  """
  def solution(self):
    """
    A list of 100 tuples of the form ((person1, person2), count) in descending order of count
    """
    #return [(('David Lauren', 'Lauren Bush'), 19)] * 100
    return [((u'Sylvester Miniter', u'Gillian Miniter'), 71), ((u'Andrew Saffir', u'Daniel Benedict'), 51), ((u'Bonnie Comley', u'Stewart Lane'), 50), ((u'Roric Tobin', u'Geoffrey Bradfield'), 49), ((u'Jamee Gregory', u'Peter Gregory'), 48), ((u'Jay Diamond', u'Alexandra Lebenthal'), 39), ((u'Somers Farkas', u'Jonathan Farkas'), 34), ((u'Martin Shafiroff', u'Jean Shafiroff'), 33), ((u'Donald Tober', u'Barbara Tober'), 31), ((u'Chappy Morris', u'Melissa Morris'), 28), ((u'Campion Platt', u'Tatiana Platt'), 27), ((u'Richard Johnson', u'Sessa von Richthofen'), 27), ((u'Lizzie Tisch', u'Jonathan Tisch'), 27), ((u'Wilbur Ross', u'Hilary Geary Ross'), 26), ((u'Deborah Norville', u'Karl Wellner'), 26), ((u'John Catsimatidis', u'Margo Catsimatidis'), 25), ((u'Chris Meigher', u'Grace Meigher'), 25), ((u'Peter Regna', u'Barbara Regna'), 25), ((u'Janna Bullock', u'Couri Hay'), 25), ((u'Julia Koch', u'David Koch'), 24), ((u'Elizabeth Stribling', u'Guy Robinson'), 24), ((u'Yaz Hernandez', u'Valentin Hernandez'), 24), ((u'Arie Kopelman', u'Coco Kopelman'), 23), ((u'Johannes Huebl', u'Olivia Palermo'), 23), ((u'Douglas Hannant', u'Frederick Anderson'), 22), ((u'Anne Hearst McInerney', u'Jay McInerney'), 21), ((u'Arlene Dahl', u'Marc Rosen'), 20), ((u'Tommy Hilfiger', u'Dee Ocleppo'), 20), ((u'James Mischka', u'Mark Badgley'), 20), ((u'Stephanie Krieger', u'Brian Stewart'), 17), ((u'Al Roker', u'Deborah Roberts'), 17), ((u'Michael Kennedy', u'Eleanora Kennedy'), 17), ((u'Fernanda Kellogg', u'Kirk Henckels'), 17), ((u'Sharon Bush', u'Jean Shafiroff'), 16), ((u'Leonel Piraino', u'Nina Griscom'), 16), ((u'Lauren Bush', u'David Lauren'), 15), ((u'Dennis Basso', u'Michael Cominotto'), 15), ((u'Donald Trump', u'Melania Trump'), 15), ((u'Diana Taylor', u'Michael Bloomberg'), 15), ((u'Francine LeFrak', u'Rick Friedberg'), 15), ((u'Anna Safir', u'Eleanora Kennedy'), 14), ((u'Randy Kemper', u'Tony Ingrao'), 14), ((u'Melanie Wambold', u'John Wambold'), 14), ((u'Clo Cohen', u'Charles Cohen'), 13), ((u'Richard Steinberg', u'Renee Steinberg'), 13), ((u'Gillian Hearst Simonds', u'Christian Simonds'), 13), ((u'Sherrell Aston', u'Muffie Potter Aston'), 13), ((u'Nicole Miller', u'Kim Taipale'), 13), ((u'Richard Farley', u'Chele Chiavacci'), 13), ((u'Dean Palin', u'Roxanne Palin'), 13), ((u'Nancy Wexler', u'Herbert Pardes'), 13), ((u'Laura Slatkin', u'Harry Slatkin'), 13), ((u'Robert Bradford', u'Barbara Taylor Bradford'), 13), ((u'Will Cotton', u'Rose Dergan'), 12), ((u'Ken Starr', u'Diane Passage'), 12), ((u'Charlotte Ronson', u'Ali Wise'), 12), ((u'Mary Davidson', u'Marvin Davidson'), 12), ((u'Susan Magazine', u'Nicholas Scoppetta'), 12), ((u'Jeff Koons', u'Justine Koons'), 12), ((u'Hunt Slonem', u'Liliana Cavendish'), 12), ((u'Elaine Langone', u'Ken Langone'), 12), ((u'Sharyn Mann', u'Todd Slotkin'), 12), ((u'Somers Farkas', u'Muffie Potter Aston'), 12), ((u'Michele Herbert', u'Larry Herbert'), 12), ((u'Gillian Miniter', u'Serena Miniter'), 12), ((u'Donna Soloway', u'Richard Soloway'), 12), ((u'Heather Matarazzo', u'Caroline Murphy'), 12), ((u'Harry Kargman', u'Jill Kargman'), 11), ((u'Alec Baldwin', u'Hilaria Baldwin'), 11), ((u'Wilbur Ross', u'Hilary Ross'), 11), ((u'Darci Kistler', u'Peter Martins'), 11), ((u'Othon Prounis', u'Kathy Prounis'), 11), ((u'Jean Shafiroff', u'Lucia Hwong Gordon'), 11), ((u'Coleman Burke', u'Susan Burke'), 11), ((u'David Yurman', u'Sybil Yurman'), 11), ((u'Urban Karlsson', u'Juan Montoya'), 11), ((u'CeCe Black', u'Lee Black'), 11), ((u'Martha Glass', u'John Glass'), 11), ((u'Keytt Lundqvist', u'Alex Lundqvist'), 11), ((u'Simon Doonan', u'Jonathan Adler'), 11), ((u'Mish Tworkowski', u'Joseph Singer'), 11), ((u'Shirin von Wulffen', u'Frederic Fekkai'), 11), ((u'Diana Taylor', u'Ana Oliveira'), 11), ((u'Daniel Benedict', u'Johannes Huebl'), 11), ((u'Simon van Kempen', u'Alex McCord'), 11), ((u'Liz Peek', u'Jeff Peek'), 11), ((u'Debbie Bancroft', u'Geoffrey Bradfield'), 10), ((u'Debbie Bancroft', u'Tiffany Dubin'), 10), ((u'Laura Lofaro Freeman', u'Jim Freeman'), 10), ((u'Andrew Roosevelt', u'Jill Roosevelt'), 10), ((u'Larry Wohl', u'Leesa Rowland'), 10), ((u'Edwina Sandys', u'Richard Kaplan'), 10), ((u'Bryant Gumbel', u'Hilary Gumbel'), 10), ((u'Arnie Rosenshein', u'Paola Rosenshein'), 10), ((u'Ralph Lauren', u'Ricky Lauren'), 10), ((u'Dan Lufkin', u'Cynthia Lufkin'), 10), ((u'Anne Ford', u'Charlotte Ford'), 10), ((u'Marc Jacobs', u'Lorenzo Martone'), 10), ((u'Carolina Herrera', u'Reinaldo Herrera'), 10), ((u'Thorne Perkin', u'Tatiana Perkin'), 10)]
  def list_length(cls):
    return 100


  @classmethod
  def tuple_validators(cls):
    return (cls.validate_tuple, cls.validate_int)
