Downloads Cragislist ads and searches them

Steps
-----

*Create sqlite3 db named ads.db*

```
CREATE TABLE tf (id INTEGER, word TEXT, cnt INTEGER, tf REAL, tfidf REAL);
CREATE TABLE ad (id INTEGER, url TEXT, title TEXT, posted INTEGER, lshash TEXT);
CREATE INDEX adididx ON ad (id);
CREATE INDEX tf_id_idx ON tf(id);
CREATE INDEX tf_word_idx ON tf(word);
```

*Create sqlite3 db named pages.db*
```
CREATE TABLE pages (url TEXT, expiry INTEGER);
CREATE UNIQUE INDEX urlidx ON pages (url);
```

*Run `python2 get_cities.py`*

This may take a while, and you may need to run it over a few days as cl will throttle (but not block).

There is a few second delay between requests.

Feel free to edit this file to grab the cities near you first and then look for the rest.

*When you're finished (or just want to search after a while) run `python3 update_tfidf.py`*

*Search with `python3 search.py <term> [<term> ...]`*

Sorts based on the sum of tfidf for all terms and how old the post is



Sad face
---------

Yes, this is a mixed python project. I had issues with beautifulsoup I hope
to workout and get to all py3
