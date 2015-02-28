import datetime
import sqlite3
import argparse
import math
from datetime import datetime
parser = argparse.ArgumentParser(description='Search CL')
parser.add_argument('term', metavar='term', type=str, nargs='+',
                   help='terms to search for')

args = parser.parse_args()
terms = "'" + "','".join(args.term) + "'"

# CREATE TABLE tf (id INTEGER, word TEXT, cnt INTEGER, tf REAL, tfidf REAL);
# CREATE TABLE ad (id INTEGER, url TEXT, title TEXT, posted INTEGER, lshash TEXT);
# CREATE INDEX adididx ON ad (id);
conn = sqlite3.connect('ads.db')

c = conn.cursor()
c.execute("""
SELECT ad.id, ad.url, ad.title, ad.posted,
       SUM(tfidf) AS ttl_tfidf,
       (strftime('%s', 'now') - posted) / 4500 AS timed
FROM ad
INNER JOIN tf
  ON     tf.id = ad.id
     AND word IN ("""+terms+""")
GROUP BY ad.id
ORDER BY (tfidf - timed);
""")

def ts2hr(ts):
    return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

row = c.fetchone()
while row is not None:
    print(ts2hr(row[3]) + "\t" + row[2] + "\t" + row[1])
    row = c.fetchone()
