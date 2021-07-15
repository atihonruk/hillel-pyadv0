from urllib.parse import urljoin, urlsplit

import requests
import lxml.html

from time import time


DOMAIN = 'http://python.org'
NETLOC = urlsplit(DOMAIN).netloc

MAX_PAGES = 40

queue = [DOMAIN]
visited = set()

count_visited = 0

with requests.Session() as session:
    while True:
        start = time()
        if count_visited > MAX_PAGES:
            break
        url = queue.pop() # !
        count_visited += 1
        res = session.get(url) # !
        if res.status_code == requests.codes.ok:
            try:
                doc = lxml.html.fromstring(res.text) # 50 Mb
            except Exception:
                print(f'Error: {url}')
            for elem, attr, link, _ in doc.iterlinks(): # href
                
                link = urljoin(DOMAIN, link)
                if not urlsplit(link).netloc == NETLOC:
                    continue
                if elem.tag == 'a' and attr == 'href':
                    if link not in visited:
                        queue.append(link) # !
                        visited.add(link) # !
        else:
            print(f'Invalid url {url} {res.status_code}')
        dur = time() - start
        print(f'Fetched {url} in {dur} s.')


print(visited)


        
