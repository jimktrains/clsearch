import urllib2
import sqlite3
import email.utils as eut
import datetime
import hashlib
import os
import gzip
import errno
from bs4 import BeautifulSoup
import cache

# CREATE TABLE pages (url TEXT, expiry INTEGER);
# CREATE UNIQUE INDEX urlidx ON pages (url);
conn = sqlite3.connect('pages.db')

def get(url):
  c = conn.cursor()
  c.execute("SELECT * FROM pages WHERE url = ?", (url,))
  row =  c.fetchone()

  utcnow = int(datetime.datetime.utcnow().strftime("%s"))
  if row is not None and row[1] > utcnow:
    c.execute("DELETE FROM pages WHERE url = ?", (url,))
    conn.commit()
    cache.remove(url)
    row = None

  if row is None:
    response = urllib2.urlopen(url)
    html = response.read()

    expiry = response.info().getheader("Expires")
    expiry = datetime.datetime(*(eut.parsedate(expiry)[0:7]))
    expiry = int(expiry.strftime("%s"))

    c.execute("INSERT INTO pages VALUES (?,?)", (url, expiry))


    cache.write(url, html)

    conn.commit()
  else:
    html = cache.get(url)
  return BeautifulSoup(html, "html5lib")

