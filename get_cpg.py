import download
from nilsimsa import Nilsimsa
import hashlib
import sqlite3
import datetime
from textblob import TextBlob
import gzip
import cache
import string
import time
from nltk.corpus import stopwords

# CREATE TABLE tf (id INTEGER, word TEXT, cnt INTEGER, tf REAL, tfidf REAL);
# CREATE TABLE ad (id INTEGER, url TEXT, title TEXT, posted INTEGER, lshash TEXT);
# CREATE INDEX adididx ON ad (id);
conn = sqlite3.connect('ads.db')

stopwords = stopwords.words('english')

def get_ads(base_url):
    c = conn.cursor()

    page = download.get(base_url + "/search/cpg")

    for p in page.select(".row"):
        pid = p['data-pid']

        a_tag = p.find('a', class_='hdrlnk')
        ad_href = a_tag['href']
        ad_title = a_tag.text

        dt = p.find('time')['datetime']
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
        dt = int(dt.strftime("%s"))

        c.execute("SELECT * FROM ad WHERE id = ?", (pid,))
        row =  c.fetchone()

        if row is None:
            url = ad_href
            if not ad_href.startswith('http'):
                url = base_url + ad_href

            time.sleep(0.5)
            ad = download.get(url)

            print url
            ad_text = ad.find(id='postingbody')
            if ad_text is None:
                if ad.find(id='has_been_removed'):
                    continue
                else:
                    raise "malformed body"
            ad_text = ad_text.text.strip()

            ad_text = filter(lambda x: x in string.printable, ad_text)
            nilsimsa = Nilsimsa(ad_text)
            lshash = nilsimsa.hexdigest()


            # c.execute("SELECT * FROM ad")
            # row = c.fetchone()
            # while row:
            #     diff = nilsimsa.compare(row[4], True)
            #     if diff < 10:
            #         print diff
            #         print cache.get("text:" + row[0])
            #         print "----"
            #         print ad_text
            #         sys.exit()

            seen = generate_word_counts(ad_text)

            cache.write("text:" + pid, ad_text)

            row = (pid, url, ad_title, dt, lshash)
            c.execute("INSERT INTO ad (id, url, title, posted, lshash) " +
                      " VALUES (?,?,?,?,?)", row)

            for word in seen:
                if word not in stopwords:
                  row = (pid, word, seen[word])
                  c.execute("INSERT INTO tf (id, word, cnt) " +
                            "VALUES (?,?,?)", row)
            conn.commit()

def generate_word_counts(ad_text):
    tb = TextBlob(ad_text)
    seen = dict()
    for word in tb.words:
        word = word.singularize().lower()
        if len(word) < 3:
            continue
        if word in seen:
            seen[word] += 1
        else:
            seen[word] = 1
    return seen
