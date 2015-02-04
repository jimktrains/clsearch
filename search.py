from nilsimsa import Nilsimsa
import datetime
import sqlite3
import argparse
import math

parser = argparse.ArgumentParser(description='Search CL')
parser.add_argument('term', metavar='term', type=str, nargs='+',
                   help='terms to search for')

args = parser.parse_args()

# CREATE TABLE tf (id INTEGER, word TEXT, cnt INTEGER);
# CREATE TABLE ad (id INTEGER, url TEXT, title TEXT, posted INTEGER, lshash TEXT);
# CREATE INDEX adididx ON ad (id);
conn = sqlite3.connect('ads.db')

c = conn.cursor()

c.execute("SELECT COUNT(*) FROM ad;")
num_posts = c.fetchone()[0]
log_num_posts = math.log(num_posts)

def tf(pid, word):
    c.execute("SELECT SUM(cnt) FROM tf WHERE id=?", (pid,))
    ttl = c.fetchone()[0]
    c.execute("SELECT cnt FROM tf WHERE id=? AND word=?", (pid,word))
    wcnt = c.fetchone()
    if wcnt:
        wcnt = wcnt[0]
        return float(wcnt) / float(ttl)
    return 0

def idf(word):
    return log_num_posts / float(1 + n_containing(word))

def tfidf(pid, word):
    return tf(pid, word) * idf(word)

def n_containing(word):
    c.execute("SELECT COUNT(*) FROM tf WHERE word=?", (word,))
    return c.fetchone()[0]

def docs_with_word(word):
    c.execute("SELECT id FROM tf WHERE word=?", (word,))
    ret = []
    row = c.fetchone()
    while row:
        ret.append(row[0])
        row = c.fetchone()
    return ret

docs = []
negs = []
for word in args.term:
    if word[0] == "-":
        word = word[1:]
    docs = docs + docs_with_word(word)
scores = dict()
for doc in docs:
    if doc not in scores:
        scores[doc] = 0
    for word in args.term:
        mod = 1
        if word[0] == "-":
            word = word[1:]
            mod = -1
        scores[doc] += (mod * tfidf(doc, word))

scores = sorted(scores.items(), key = lambda x : -x[1])

for score in scores:
    c.execute("SELECT * FROM ad WHERE id = ?", (score[0],))
    row = c.fetchone()
    print row[2] + "\t" + row[1] + "\t"
