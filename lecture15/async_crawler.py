import asyncio

from urllib.parse import urljoin, urlsplit

import aiohttp
import lxml.html

MAX_PAGES = 40

NUM_WORKERS = 100
DOMAIN = 'http://python.org'
NETLOC = urlsplit(DOMAIN).netloc

enqueued = set()
count_visited = 0


async def worker(n, session, queue):
    global count_visited
    while True:
        if count_visited >= MAX_PAGES:
            break

        count_visited += 1
        url = await queue.get()
        async with await session.get(url) as res:
            if res.status != 200:
                continue
            try:
                txt = await res.text() # socket.recv()
            except Exception as e:
                print(e)
                continue
            doc = lxml.html.fromstring(txt) # alloc
            for elem, attr, link, _ in doc.iterlinks():
                link = urljoin(DOMAIN, link)
                if not urlsplit(link).netloc == NETLOC:
                    continue
                if elem.tag == 'a' and attr == 'href':
                    if link not in enqueued:
                        enqueued.add(link)
                        queue.put_nowait(url)   



async def start():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        queue = asyncio.Queue()
        queue.put_nowait(DOMAIN)
        workers = [worker(n, session, queue) for n in range (10)]
        await asyncio.gather(*workers) 


asyncio.run(start())
print(enqueued)
