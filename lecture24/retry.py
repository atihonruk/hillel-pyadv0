from time import sleep


def constant_wait(sec):
    return lambda _: sec


no_wait = constant_wait(0)


def exponential_wait(attempt):
    return 2 ** attempt - 1


def retry(max_attempts=3, wait_fn=no_wait, exceptions=(Exception,)):
    def outer(fn):
        def inner(*args, **kwargs):
            ex = None
            for n in range(max_attempts):
                wait_sec = wait_fn(n)
                sleep(wait_sec)
                print(f'Attempt #{n}, delay: {wait_sec}')
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    ex = e
            raise ex
        return inner
    return outer
 


if __name__ == '__main__':
    import requests
    
    @retry(max_attempts=5, wait_fn=exponential_wait)
    def get_data():
        res = requests.get("http://httpbin.org/status/404")
        print(f'Status: {res.status_code}')
        res.raise_for_status()

    get_data()
