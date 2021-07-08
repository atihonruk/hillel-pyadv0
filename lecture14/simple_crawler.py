from urllib.parse import urljoin, urlsplit

import requests
import lxml.html


DOMAIN = 'http://python.org'
NETLOC = urlsplit(DOMAIN).netloc

MAX_PAGES = 20

queue = [DOMAIN]
visited = set()

count_visited = 0

with requests.Session() as session:
    while True:
        if count_visited > MAX_PAGES:
            break
        url = queue.pop()
        print(url)
        count_visited += 1
        res = session.get(url)
        if res.status_code == requests.codes.ok:
            try:
                doc = lxml.html.fromstring(res.text)
            except Exception:
                print(f'Error: {url}')
            for elem, attr, link, _ in doc.iterlinks(): # href
                
                link = urljoin(DOMAIN, link)
                if not urlsplit(link).netloc == NETLOC:
                    continue
                if elem.tag == 'a' and attr == 'href':
                    if link not in visited:
                        queue.append(link)
                        visited.add(link)
        else:
            print(f'Invalid url {url} {res.status_code}')

print('###')
for url in visited:
    print(url)

        
