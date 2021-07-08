import asyncio
from threading import Thread, Lock

# Demonstrates that inplace_add (+=) is not thread safe.

_counter = 0

# lock = Lock()

def incr():
    global _counter

    for _ in range(1000):
        # with lock:
            for _ in range(1000):
                _counter += 1


def show_count():
    global _counter
    threads = [Thread(target=incr) for t in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(_counter)



# Visualization of the concurrent execution
# of two threads vs two coroutines


# Threads

def task(n):
    for x in range(10):
        for y in range(10):
            print(f'Thread #{n}: {x} {y}')


def run_threads():
    t1 = Thread(target=task, args=(1,))
    t2 = Thread(target=task, args=(2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


# Coroutines
    
async def atask(n):
    for x in range(10):
        # await asyncio.sleep(0.001)
        for y in range(10):
            print(f'Coroutine #{n}: {x} {y}')


def run_coros():
    async def main():
        await asyncio.gather(atask(1), atask(2))

    asyncio.run(main())


# show_count()
# run_threads()
# run_coros()
