from nilsimsa import Nilsimsa
import datetime
import sqlite3
import argparse
import math

# CREATE TABLE tf (id INTEGER, word TEXT, cnt INTEGER, tf REAL, tfidf REAL);
# CREATE TABLE ad (id INTEGER, url TEXT, title TEXT, posted INTEGER, lshash TEXT);
# CREATE INDEX adididx ON ad (id);
conn = sqlite3.connect('ads.db')
conn.create_function('ln', 1, math.log);

c = conn.cursor()

print "Creating wcnt"
c.execute("DROP TABLE IF EXISTS wcnt;")
c.execute("CREATE TABLE wcnt AS SELECT id, sum(cnt) AS wcnt  FROM tf GROUP BY id;")
c.execute("CREATE index wcnt_id_idx ON wcnt (id);")

print "Creating idf"
c.execute("DROP TABLE IF EXISTS idf;")
c.execute("""CREATE TABLE idf AS
    SELECT ln(  (SELECT CAST(COUNT(*) AS real) FROM wcnt)
              / CAST((1 + (SELECT COUNT(*) FROM tf bar WHERE bar.word = foo.word)) AS REAL)) AS idf,
           word
    FROM tf AS foo
    GROUP BY word;""")
c.execute("CREATE index idf_word ON idf(word);")

print "Calculating tf"
c.execute("""UPDATE tf SET
    tf =   CAST(cnt AS REAL)
         / (SELECT CAST(wcnt AS REAL) FROM wcnt AS foo WHERE foo.id = tf.id);""")

print "Calculating tfidf"
c.execute("UPDATE tf SET tfidf = tf * (SELECT idf FROM idf WHERe idf.word = tf.word);")

