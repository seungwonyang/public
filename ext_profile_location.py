# Filename: ext_profile_location.py
# Description:         
# shell>python text_profile_location.py
# Name: Seungwon Yang  <seungwon@vt.edu>

import sys 
import string
import re
import MySQLdb
import urllib2
import codecs
from bs4 import BeautifulSoup

#---------------- class ---------------------#
class ExtProfileLocation:
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

  def removeSymbols(self, word):
    return re.sub(r'[^\w]', ' ', word)

  def processTweet(self, cur, table):
    cur.execute("select id,from_user from " + table)
    for row in cur.fetchall():

      row_id = row[0]
      from_user = row[1]
      print "\n------------------- row: %d ---------------------\n" % row_id
      print row_id
      print from_user

      # download tweet page
      profile_web = "http://www.twitter.com/" + from_user
      try:
        content = urllib2.urlopen(profile_web).read()
        soup = BeautifulSoup(content)
        # print(soup.prettify())

        for item in soup.find_all("span", "location"):
          location = item.text.strip()
          print location
          query = "update " + table + " set location='" +location+ "' where id='" + str(row_id) + "'"
          cur.execute(query)
      # get location text   <span class="location">
      except:
        pass

#---------------- main -----------------------#
def main():
  host = "db_host_name"
  db = "db_name"
  user = "db_user_name"
  passwd = "db_passwd"
  table = "db_table_name"
  epl = ExtProfileLocation()
  cur = epl.connectMysql(host, user, passwd, db)
  epl.processTweet(cur, table)


if __name__ == "__main__":
  main()


  
