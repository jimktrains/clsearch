#!/usr/bin/env python2

import download
import get_cpg
import re
import random

page = download.get("http://www.craigslist.org/about/sites");

alst = page.find_all('a')

random.shuffle(alst)

for a in alst:
    if 'name' in a.attrs:
        if a['name'] != 'US':
            break;
    if 'href' in a.attrs:
        g = re.match('http://[^\.]+\.craigslist.org', a['href'])
        if g:
            get_cpg.get_ads(g.group(0))
