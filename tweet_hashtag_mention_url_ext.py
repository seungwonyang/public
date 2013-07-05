# Filename: tweet_hashtag_mention_url_ext.py
# Description: This scripts extracts hashtags, @mentions, and URLs from tweets stored in a db. Then,
#              add the extracted data back to the db.      
# shell>python tweet_hashtag_mention_url_ext.py
# Name: Seungwon Yang  <seungwon@vt.edu>


import sys 
import string
import re
import MySQLdb
from bs4 import BeautifulSoup

#---------------- class ---------------------#
class TweetCleaner:
  def __init__(self):
    # prepare stopword list
    
    sfi = open('stopwords.txt', 'r').read()
    sfi2 = open('custom_stops.txt', 'r').read()
    self.stoplist = list(set(sfi.split() + sfi2.split()))

  def connectMysql(self, host, user, passwd, db):
    # connect
    db = MySQLdb.connect(host, user, passwd, db)
    # create a cursor
    cur = db.cursor()
    # return cursor
    return cur

  def removeExtraSpaces(self, data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)

  def removeSymbols(self, word):
    return re.sub(r'[^\w]', ' ', word)

  def checkRT(self, tweet_text):
    if (tweet_text[0:3] == "RT "):
      return 1
    else:
      return 0

  def extractMentions(self, tweet_text):
    mentions = re.findall("(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z_]+[A-Za-z0-9_]+)", tweet_text)
    return mentions

  def extractHashtags(self, tweet_text):
    hashtags = re.findall("(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z_]+[A-Za-z0-9_]+)", tweet_text)
    return hashtags

  def extractCleantext(self, tweet_text, hashtags_li, mentions_li, urlli):
    cleaned_text = tweet_text
    cleaned_text_li =[]
    for item in hashtags_li:
      cleaned_text = cleaned_text.replace(item, " ")
    for item2 in mentions_li:
      cleaned_text = cleaned_text.replace(item2, " ")
    for item3 in urlli:
      cleaned_text = cleaned_text.replace(item3, " ")
    # remove symbols
    cleaned_text = self.removeSymbols(cleaned_text)
    
    for word in cleaned_text.split():
      if len(word) > 1 and (word.lower() not in self.stoplist):
        cleaned_text_li.append(word.lower())    

    return cleaned_text_li 

  def extractUrls(self, tweet_text):
    urlli = re.findall("(?P<url>https?://[^\s]+)", tweet_text)
    return urlli

  def processTweet(self, cur, table):
    # cur.execute("select id,text from " + table + " limit 100")
    cur.execute("select id,text from " + table)
    i = 1
    for row in cur.fetchall():
      tmp_text = ""
      clean_text_li = []
      hashtags_li = []
      mentions_li = []
      language = ""
      tweet_id = row[0]
      text = row[1]
      print "\n------------------- row: %d ---------------------\n" % tweet_id
      # print text
      is_rt = self.checkRT(text)
      mentions_li = self.extractMentions(text)
      hashtags_li = self.extractHashtags(text)
      urlli = self.extractUrls(text)
      clean_text_li = self.extractCleantext(text, hashtags_li, mentions_li, urlli)
      
      # join
      hashtags = ",".join(hashtags_li)
      mentions = ",".join(mentions_li)
      clean_text = " ".join(clean_text_li)
      # print hashtags
      # print mentions
      # print clean_text
      i += 1
      query = "update " + table + " set is_rt=" + str(is_rt) +", clean_text='" +clean_text+ "', hashtags='"+hashtags+"', mentions='"+mentions+"' where id=" + str(tweet_id)
      cur.execute(query)



#---------------- main -----------------------#
def main():
  host = "host_name"
  db = "db_name"
  user = "db_user_id"
  passwd = "db_passwd"
  table = "db_table_name"
  tc = TweetCleaner()
  cur = tc.connectMysql(host, user, passwd, db)
  tc.processTweet(cur, table)


if __name__ == "__main__":
  main()


  
