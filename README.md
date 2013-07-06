Brief description of the files in this repository:

custom_stops.txt
 :it contains custom-added stop words

ext_profile_location.py
 :it extracts Twitter user's location by visiting 
  the users' Twitter page

lda_isaac12_resources.py
 :it runs LDA algorithm on a bunch of tweets about
  Hurricane Isaac disaster in 2012, then generates
  word groups, each of which represent hidden topic

mongoNYT.py
 :it can be used to (1)extract JSON from Solr;
  (2) add JSON to either MongoDB or MySQL db

phasevis_index.html
 :this is a prototype visualization interface for
  Hurricane Isaac tweet classification/visualization
  (http://spare05.dlib.vt.edu/~ctrvis/phasevis/index_may.html)

provis.css
 :css file related to provis visualization

provis_index.html
 :prototype user interface for visual analytics, which 
  communicates with Solr indexing engine in the backend.
  It also uses JSON files containing topic relatedness.

stopwords.txt
 :general stopwords for text processing

tweet_hashtag_mention_url_ext.py
 :it extracts hashtags, @mentions, and embedded shortened
  URLs from tweet text and writes them into MySQL db
