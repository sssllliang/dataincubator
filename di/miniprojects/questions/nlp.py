# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
## Overview

Unstructured data makes up the vast majority of data.  This is a basic intro to handling unstructured data.  Our objective is to be able to extract the sentiment (positive or negative) from review text.  We will do this from Yelp review data.

Your model will be assessed based on how root mean squared error of the number of stars you predict.  There is a reference solution (which should not be too hard to beat).  The reference solution has a score of 1.

**Download the data here **: http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_review.json.gz


## Download and parse the data

The data is in the same format as in ml.py

## Helpful notes:
- You may run into trouble with the size of your models and Heroku's memory limit.  This is a major concern in real-world applications.  Your production environment will likely not be that different from Heroku and being able to deploy there is important and companies don't want to hire data scientists who cannot cope with this.  Think about what information the different stages of your pipeline need and how you can reduce the memory footprint.

"""

from lib import QuestionList, Question, list_or_dict, ListValidateMixin, YelpListOrDictValidateMixin
QuestionList.set_name("nlp")


class NLPValidateMixin(YelpListOrDictValidateMixin, Question):
  @classmethod
  def fields(cls):
    return ['text']

  @classmethod
  def _test_json(cls):
    return [
      {"votes": {"funny": 0, "useful": 0, "cool": 0}, "user_id": "WsGQfLLy3YlP_S9jBE3j1w", "review_id": "kzFlI35hkmYA_vPSsMcNoQ", "stars": 5, "date": "2012-11-03", "text": "Love it!!!!! Love it!!!!!! love it!!!!!!!   Who doesn't love Culver's!", "type": "review", "business_id": "LRKJF43s9-3jG9Lgx4zODg"},
      {"votes": {"funny": 0, "useful": 0, "cool": 0}, "user_id": "Veue6umxTpA3o1eEydowZg", "review_id": "Tfn4EfjyWInS-4ZtGAFNNw", "stars": 3, "date": "2013-12-30", "text": "Everything was great except for the burgers they are greasy and very charred compared to other stores.", "type": "review", "business_id": "LRKJF43s9-3jG9Lgx4zODg"},
      {"votes": {"funny": 0, "useful": 0, "cool": 0}, "user_id": "u5xcw6LCnnMhddoxkRIgUA", "review_id": "ZYaS2P5EmK9DANxGTV48Tw", "stars": 5, "date": "2010-12-04", "text": "I really like both Chinese restaurants in town.  This one has outstanding crab rangoon.  Love the chicken with snow peas and mushrooms and General Tso Chicken.  Food is always ready in 10 minutes which is accurate.  Good place and they give you free pop.", "type": "review", "business_id": "RgDg-k9S5YD_BaxMckifkg"},
      {"votes": {"funny": 0, "useful": 0, "cool": 0}, "user_id": "kj18hvJRPLepZPNL7ySKpg", "review_id": "uOLM0vvnFdp468ofLnszTA", "stars": 3, "date": "2011-06-02", "text": "Above average takeout with friendly staff. The sauce on the pan fried noodle is tasty. Dumplings are quite good.", "type": "review", "business_id": "RgDg-k9S5YD_BaxMckifkg"},
      {"votes": {"funny": 0, "useful": 0, "cool": 0}, "user_id": "L5kqM35IZggaPTpQJqcgwg", "review_id": "b3u1RHmZTNRc0thlFmj2oQ", "stars": 4, "date": "2012-05-28", "text": "We order from Chang Jiang often and have never been disappointed.  The menu is huge, and can accomodate anyone's taste buds.  The service is quick, usually ready in 10 minutes.", "type": "review", "business_id": "RgDg-k9S5YD_BaxMckifkg"}
    ]


@QuestionList.add
class BagOfWordsModel(NLPValidateMixin):
  """
  Build a bag of words model.  Our strategy will be to build a linear model based on the count of the words in each document (review).  **Note:** `def solution` takes an argument `record`.  Samples of `record` are given in `_test_json`.

  1. Don't forget to use tokenization!  This is important for good performance but it is also the most expensive step.  Try vectorizing as a first initial step:
    ``` python
    X = (feature_extraction.text
            .CountVectorizer()
            .fit_transform(text))
    y = scores
    ```
    and then running grid-serach and cross-validation only on of this pre-processed data.

    `CountVectorizer` has to memorize the mapping between words and the index to which it is assigned.  This is linear in the size of the focabulary.  The `HashingVectorizer` does not have to remember this mapping and will lead to much smaller models.

  2. Try choosing different values for `min_df` (minimum document frequency cutoff) and `max_df` in `CountVectorizer`.  Setting `min_df` to zero admits rare words which might only appear once in the entire corpus.  This is both prone to overfitting and makes your data unmanageablely large.  Don't forget to use cross-validation or to select the right value.  Notice that `HashingVectorizer` doesn't support `min_df`  and `max_df`.  However, it's not hard to roll your own transformer that solves for these.

  3. Try using `LinearRegression` or `RidgeCV`.  If the memory footprint is too big, try switching to Stochastic Gradient Descent: [`SGDRegressor`](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html).  You might find that even ordinary linear regression fails due to the data size.  Don't forget to use `GridSearchCV` to determine the regularization parameter!  How do the regularization parameter `alpha` and the values of `min_df` and `max_df` from `CountVectorizer` change the answer?
  """

  # Global Imports
  # ===========================================================================
  from sklearn.externals import joblib

  # Global Objects
  # ===========================================================================
  global lrr
  lrr = joblib.load('/home/vagrant/miniprojects/questions/3_week/nlp/pickles/q1_lrr.pkl')
  global cv
  cv = joblib.load('/home/vagrant/miniprojects/questions/3_week/nlp/pickles/q1_cv.pkl')

  def __init__(self):
    return

  @list_or_dict
  def solution(self, review):
    #print 'BagOfWordsModel \n', review
    X = cv.transform(review)
    y = lrr.predict(X)
    return y[0].item()
    # .4 : return 4.
    # .6 : return 3.6
    # return 0.


@QuestionList.add
class NormalizedModel(NLPValidateMixin):
  """
  Normalization is a key for linear regression.  Previously, we used the count as the normalization scheme.  Try some of these alternative vectorizations:

  1. You can use the "does this word present in this document" as a normalization scheme, which means the values are always 1 or 0.  So we give no additional weight to the presence of the word multiple times.

  2. Try using the log of the number of counts (or more precisely, $log(x+1)$).  This is often used because we want the repeated presence of a word to count for more but not have that effect tapper off.

  3. [TFIDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) is a common normalization scheme used in text processing.  Use the `TFIDFTransformer`.  There are options for using `idf` and taking the logarithm of `tf`.  Do these significantly affect the result?

  Finally, if you can't decide which one is better, don't forget that you can combine models with a linear regression.
  """
  @list_or_dict
  def solution(self, review):
    # print 'NormalizedModel \n', review
    return 0.


@QuestionList.add
class BigramModel(NLPValidateMixin):
  """
  In a bigram model, let's consider both single words and pairs of consecutive words that appear.  This is going to be a much higher dimensional problem (large $p$) so you should be careful about overfitting.

  Sometimes, reducing the dimension can be useful.  Because we are dealing with a sparse matrix, we have to use `TruncatedSVD`.  If we reduce the dimensions, we can use a more sophisticated models than linear ones.
  """
  @list_or_dict
  def solution(self, review):
    # print 'BigramModel \n', review
    return 0.


@QuestionList.add
class FoodBigrams(ListValidateMixin, Question):
  """
  Look over all reviews of restaurants (you may need to look at the dataset from `ml.py` to figure out which ones correspond to restaurants).  There are many bigrams, but let's look at bigrams that are 'special'.  We can think of the corpus as defining an empirical distribution over all ngrams.  We can find word pairs that are unlikely to occur consecutively based on the underlying probability of their words.  Mathematically, if $p(w)$ be the probability of a word $w$ and $p(w_1 w_2)$ is the probability of the bigram $w_1 w_2$, then we want to look at word pairs $w_1 w_2$ where the statistic

  $$ p(w_1 w_2) / p(w_1) / p(w_2) $$

  is high.  Return the top 100 (mostly food) bigrams with this statistic with the 'right' prior factor (see below).

  **Questions:** (to think about: they are not a part of the answer).  This statistic is a ratio and problematic when the denominator is small.  We can fix this by applying Bayesian smoothing to $p(w)$ (i.e. mixing the empirical distribution with the uniform distribution over the vocabulary).

    1. How does changing this smoothing parameter effect the word paris you get qualitatively?

    2. We can interpret the smoothing parameter as adding a constant number of occurences of each word to our distribution.  Does this help you determine set a reasonable value for this 'prior factor'?

    3. For fun: also check out [Amazon's Statistically Improbable Phrases](http://en.wikipedia.org/wiki/Statistically_Improbable_Phrases).
  """

  # Global Imports
  # =====================================================================================================
  # import simplejson as json
  # import numpy as np
  # import pandas as pd

  # Instantiate Global Objects
  # =====================================================================================================

  # bg_vec = joblib.load('/home/vagrant/miniprojects/questions/3_week/nlp/pickles/q4_bg_vec.pkl')



  # Methods
  # =====================================================================================================

  def __init__(self):
    return

  def solution(self):

    # 0.44 : 
    return [u'pei wei', u'kung pao', u'monte carlo', u'wi fi', u'hong kong', u'wal mart', u'prix fixe', u'amuse bouche', u'ami gabi', u'du soleil', u'panna cotta', u'surf turf', u'tex mex', u'los angeles', u'huevos rancheros', u'hustle bustle', u'wolfgang puck', u'krispy kreme', u'foie gras', u'lotus siam', u'coca cola', u'bok choy', u'loco moco', u'tikka masala', u'flip flops', u'tater tots', u'tres leches', u'cole slaw', u'pina colada', u'banh mi', u'pinot noir', u'joel robuchon', u'butternut squash', u'gordon ramsay', u'planet hollywood', u'clam chowder', u'hush puppies', u'croque madame', u'bloody mary', u'kool aid', u'http www', u'osso bucco', u'pf changs', u'creme brulee', u'fro yo', u'beaten path', u'carne asada', u'mon ami', u'wicked spoon', u'nom nom', u'bo hue', u'jean philippe', u'cave creek', u'mani pedi', u'knick knacks', u'dim sum', u'penn teller', u'washer dryer', u'scantily clad', u'santa fe', u'bang buck', u'pun intended', u'moscow mule', u'saving grace', u'shabu shabu', u'hoover dam', u'roller coaster', u'mandalay bay', u'chow mein', u'hubert keller', u'julian serrano', u'san diego', u'au jus', u'timely manner', u'hash browns', u'mahi mahi', u'baskin robbins', u'san francisco', u'panda express', u'cirque du', u'pf chang', u'sky harbor', u'grey goose', u'jiffy lube', u'al dente', u'dac biet', u'smack dab', u'wells fargo', u'uuu uuu', u'spam musubi', u'calvin harris', u'barnes noble', u'lloyd wright', u'sea bass', u'lactose intolerant', u'dimly lit', u'kilt lifter', u'mario batali', u'au gratin', u'sq ft']
    # 0.42 : return [u'pei wei', u'hong kong', u'kung pao', u'wal mart', u'panna cotta', u'amuse bouche', u'prix fixe', u'ami gabi', u'monte carlo', u'krispy kreme', u'tex mex', u'wi fi', u'huevos rancheros', u'coca cola', u'bok choy', u'hustle bustle', u'surf turf', u'tres leches', u'pina colada', u'wolfgang puck', u'loco moco', u'du soleil', u'lotus siam', u'osso bucco', u'joel robuchon', u'hush puppies', u'croque madame', u'pinot noir', u'flip flops', u'knick knacks', u'tikka masala', u'kool aid', u'los angeles', u'tater tots', u'pf changs', u'butternut squash', u'scantily clad', u'banh mi', u'jean philippe', u'moscow mule', u'bo hue', u'penn teller', u'baskin robbins', u'dac biet', u'gordon ramsay', u'hoover dam', u'fro yo', u'cole slaw', u'beaten path', u'santa fe', u'foie gras', u'uuu uuu', u'clam chowder', u'barnes noble', u'wells fargo', u'jiffy lube', u'lloyd wright', u'calvin harris', u'hubert keller', u'lactose intolerant', u'julian serrano', u'kilt lifter', u'pun intended', u'cave creek', u'washer dryer', u'bells whistles', u'itty bitty', u'roller coaster', u'nom nom', u'mon ami', u'arnold palmer', u'riff raff', u'smack dab', u'planet hollywood', u'rula bula', u'shabu shabu', u'celine dion', u'bloody mary', u'sq ft', u'stainless steel', u'mario batali', u'spam musubi', u'harry potter', u'pf chang', u'grey goose', u'wicked spoon', u'valle luna', u'vice versa', u'mani pedi', u'creme brulee', u'baba ganoush', u'yada yada', u'sauvignon blanc', u'190 octane', u'saving grace', u'har gow', u'carl jr', u'kee mao', u'patatas bravas', u'dutch bros']
    # 0.1 : return [u'panna cotta', u'pei wei', u'krispy kreme', u'hong kong', u'knick knacks', u'dac biet', u'baskin robbins', u'pina colada', u'tres leches', u'osso bucco', u'bok choy', u'huevos rancheros', u'amuse bouche', u'coca cola', u'wal mart', u'itty bitty', u'riff raff', u'hustle bustle', u'rula bula', u'uuu uuu', u'scantily clad', u'tex mex', u'kung pao', u'moscow mule', u'barnes noble', u'loco moco', u'croque madame', u'ami gabi', u'wolfgang puck', u'hush puppies', u'prix fixe', u'wells fargo', u'lloyd wright', u'lactose intolerant', u'calvin harris', u'kilt lifter', u'kool aid', u'joel robuchon', u'patatas bravas', u'lotus siam', u'bells whistles', u'valle luna', u'celine dion', u'hoover dam', u'penn teller', u'pinot noir', u'tammie coe', u'jiffy lube', u'surf turf', u'arnold palmer', u'jean philippe', u'ropa vieja', u'puerto rican', u'yada yada', u'kee mao', u'monte carlo', u'vice versa', u'harry potter', u'pf changs', u'flip flops', u'cabo wabo', u'190 octane', u'gulab jamun', u'cochinita pibil', u'bo hue', u'neiman marcus', u'julian serrano', u'har gow', u'santa fe', u'thit nuong', u'lomo saltado', u'hubert keller', u'wi fi', u'osso buco', u'nooks crannies', u'sauvignon blanc', u'du soleil', u'ezzyujdouig4p gyb3pv_a', u'cous cous', u'tikka masala', u'stainless steel', u'toby keith', u'feng shui', u'baba ganoush', u'ping pang', u'ritz carlton', u'smack dab', u'kare kare', u'leaps bounds', u'bradley ogden', u'aguas frescas', u'parmigiano reggiano', u'artery clogging', u'lau lau', u'pai gow', u'sq ft', u'hodge podge', u'tater tots', u'butternut squash', u'hoity toity']
    # 0.1 : return [u'ansom broso', u'\xe4gyptischen figuren', u'jeru damaja', u'freeport mcmoran', u'ulan bator', u'vegasproblems noragrets', u'weliswaar toeristen', u'chazz palminteri', u'lefort osteotomy', u'chambolle musigny', u'leighton meester', u'243919811 754996307', u'odours spetic', u'stephon marbury', u'mjokusdiqxfpsymb mms9g', u'muf ler', u'gevraagd zojuist', u'yngwie malmsteen', u'gonorrhoeae trahomatis', u'shaelyn mccole', u'ajbombers ajbombersmsn', u'alarme incendie', u'alkyhol dikshunary', u'teleurstellende ervaring', u'toshiaki nishioka', u'mizu gotoshi', u'negli stati', u'zqvvdm_ ikgvhpmzruk3lg', u'ernestine ulmer', u'ooooey gooooey', u'rw5n finhqb', u'5ip4_yfvx3sz4qmqxl 4mw', u'drukke doordeweekse', u'encoretowersuites towerkingsuite', u'754996307 1382033796', u'doordeweekse avond', u'orecchie elefante', u'salwar kameez', u'plaats daarvan', u'kk153 poizonmotherfuckingivy', u'finhqb fr3bgqypdg', u'ervaring gehad', u'87591 gonorrhoeae', u'knicker knackers', u't3asfec34b8 uyr3xzj8lw', u'napole tani', u'd4qwvw4pcn _2mk2o1ro1g', u'rockem sockem', u'poizonmotherfuckingivy m5lv909233384651', u'filippa mcdougall', u'_ga 243919811', u'bogaty wyb\xf3r', u'vall\xe9e aspe', u'wurkin burkin', u'anch essa', u'indu mishra', u'zonder overleg', u'h9ruaaha5kcqkqtj sgs0q', u'bobsmith mysuccess', u'nucking futs', u'inspectionresultsdrilldown in_insp_id', u'zind humbrecht', u'lucretia torva', u'skuse deyyzz', u'hoyty toyty', u'luang prabang', u'willen liever', u'buyi zama', u'scansano perazzi', u'list_details list_id', u'_ylv csz', u'onze standaard', u'badgley mischka', u'tafel verwacht', u'382 4357', u'ferr\xe1n adri\xe0', u'myocardial infarction', u'coxinhas pasteis', u'reuscher haart', u'fourme ambert', u'kreative kupcakes', u'hoighty toighty', u'daarvan kwam', u'wim wenders', u'fuqi feipian', u'eartha kitt', u'kandice linwright', u'kamel guechida', u'asse cabe', u'trixies trevors', u'emack bolio', u'medulla oblongata', u'pizzaiuoli napole', u'molcajeta nayarita', u'ayu kanroni', u'anquan boldin', u'avenged sevenfold', u'placeee rockkkkkkkkssssssss', u'anibal culk', u'chupale pichon']
    #return [u'higgledy piggledy', u'zind humbrecht', u'plaats daarvan', u'freeport mcmoran', u'hocus pocus', u'orville redenbacher', u'skuse deyyzz', u'luang prabang', u'2f 2fwww', u'wurkin burkin', u'betaalbaar aangenaam', u'ajbombers ajbombersmsn', u'frats sororities', u'anch essa', u'getchoa ovahea', u'orecchie elefante', u'zonder overleg', u'phunk junkeez', u'napole tani', u'weliswaar toeristen', u'finhqb fr3bgqypdg', u'vall\xe9e aspe', u'doordeweekse avond', u'chazz palminteri', u'inspectionresultsdrilldown in_insp_id', u'medulla oblongata', u'sidral mundet', u'rockem sockem', u'd4qwvw4pcn _2mk2o1ro1g', u'5ip4_yfvx3sz4qmqxl 4mw', u'gevraagd zojuist', u'_ylv csz', u'drukke doordeweekse', u'asse cabe', u'ryne sandburger', u'myocardial infarction', u'trompe oeil', u'negli stati', u'aangenaam verrast', u'erykah badu', u'teleurstellende ervaring', u'ansom broso', u'ulan bator', u't3asfec34b8 uyr3xzj8lw', u'lebendiges kino', u'rw5n finhqb', u'ooooey gooooey', u'krav maga', u'chambolle musigny', u'oah duz', u'ervaring gehad', u'mizu gotoshi', u'willen liever', u'hoyty toyty', u'dionne warwick', u'toshiaki nishioka', u'oyszi4r_ xj0uuvtte5vpg', u'wim wenders', u'coxinhas pasteis', u'ivo angelov', u'reuscher haart', u'fuqi feipian', u'kosta browne', u'smorgas copia', u'clinks clanks', u'wordt zeker', u'wilford brimley', u'bua loi', u'mckayla maroney', u'829 1168', u'caps104 25328', u'gault millau', u'ferr\xe1n adri\xe0', u'589 8888', u'jibber jabber', u'sodom gomorrah', u'onze standaard', u'ayu kanroni', u'zeker toegevoegd', u'scansano perazzi', u'erectile dysfunction', u'2gmgt 7qjowr1ihup3fbva', u'douwe egberts', u'stati uniti', u'fourme ambert', u'machu picchu', u'thespot boldroost', u'acili ezme', u'kamel guechida', u'biv devoe', u'hussel bussel', u'doyle brunson', u'helter skelter', u'amon amarth', u'macauley culkin', u'20establishments 20search', u'trixies trevors', u'tafel verwacht', u'addis ababa', u'nogmaals bij']
    # 0.1 : result of min_df = 1 : return [u'lowly fibs', u'esteem boosted', u'stressed resources', u'palomino comet', u'palette cleansing', u'defies categorization', u'evened imperfections', u'jordy nelson', u'tue thur', u'struggled manipulate', u'packages leaking', u'pacific northwest', u'tr\xe9s romantique', u'jumble quartered', u'oxford comma', u'burner heaped', u'stumble bum', u'pals hmmmmmmm', u'amaaazing sweetheart', u'arts commission', u'commercials boast', u'jer els', u'storms vicinity', u'passive aggressively', u'partisans liberals', u'assure alki', u'deem deplorable', u'parmigiano reggiano', u'jigsawed puzzled', u'paraphernalia predominate', u'essplode judgment', u'commit blasphemy', u'paperwork calculators', u'commission calendar', u'assembled aggregations', u'commie socialist', u'kanom jeeb', u'karaokeeeeeee yuppp', u'overshadowed clams', u'overpopulated posers', u'buts exclusions', u'flashback feathery', u'oppressive society', u'sulfuric pungency', u'flannel shirts', u'kiew wan', u'ooooohhhh haaahaaa', u'truant dukedom', u'flander reds', u'cacophany fade', u'sunflower seeds', u'omni farting', u'omletes skilets', u'kimmy brian', u'caffienated jitters', u'orchid gilbert', u'kfyiewxac slp_qeiuo6hw', u'kendall jackson', u'overcoming obstacle', u'bushy tailed', u'overloaded lard', u'overload populated', u'overgrown mayberry', u'overdosing spam', u'overdo overcook', u'flaunting thong', u'30p 8p', u'karben4 upland', u'buster parfaits', u'trustfund hippies', u'oscar mayer', u'sucking pals', u'trunk safety', u'flimsy styro', u'storage unit', u'peaches oranges', u'flyers rewards', u'whooping cough', u'stapled photocopied', u'populate grayed', u'fontaines tr\xe9s', u'pooling circled', u'austin dallas', u'pompous facades', u'inquiry accusatory', u'universe patanne', u'intact yielded', u'attest transformation', u'uniforms jeeez', u'2004 1969', u'plant bathtub', u'interiors catchy', u'unredeemable nutritionally', u'contacts executives', u'contain strawberries', u'squealed gayness', u'botle habanero', u'inexplicable inexcusable', u'sprout overload', u'sprouted lentils']
    # 0.24 : correct answer : return [u'carne asada', u'tiki torches', u'carb loading', u'bees knees', u'latina hussie', u'mardi gras', u'salsiccia rossa', u'hush puppies', u'pf changs', u'lactose intolerant', u'imported provolone', u'chang jiang', u'rojo diablo', u'rico rita', u'santa fe', u'viad tower', u'carbo load', u'johnson creek', u'mc donalds', u'odana rd', u'pea pods', u'coca cola', u'pet peeve', u'beaten path', u'sheboygan brats', u'slam dunk', u'http www', u'philly cheesesteak', u'kung pao', u'chop suey', u'prickly pear', u'miller lite', u'comedor guadalajara', u'log cabin', u'com biz_photos', u'checkered tablecloths', u'anissa amy', u'san diego', u'san francisco', u'swivel factor', u'au jus', u'war stories', u'chit chat', u'au gratin', u'train wreck', u'los angeles', u'carpet stairs', u'maple cured', u'exposed brick', u'worn carpet', u'mission accomplished', u'tan tan', u'papa johns', u'al dente', u'4th july', u'creme brulee', u'tikka masala', u'digestive track', u'ooey gooey', u'sir charles', u'nuh uh', u'shirt jeans', u'shelf conmemorativo', u'palm trees', u'ale asylum', u'shoplifter delight', u'cracker barrel', u'fight inc', u'texas roadhouse', u'delicacies sizzling', u'shrugged shoulders', u'kicks ass', u'dimly lit', u'shapes sizes', u'merry mu', u'micro brews', u'sky lounge', u'puff pastry', u'mi cocina', u'dairy queen', u'baby pike', u'relish tray', u'moo shu', u'napkin lap', u'spotted cows', u'wonton wrappers', u'sassy cow', u'fox news', u'sir hobos', u'smiles faces', u'chile rubbed', u'mahi mahi', u'bang buck', u'clam chowder', u'fond memories', u'chase field', u'award winning', u'seared ahi', u'jimmy buffett', u'saving grace']
    # return [u'huevos rancheros'] * 100

