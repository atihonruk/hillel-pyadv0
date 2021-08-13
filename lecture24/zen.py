import this

from datetime import datetime
from random import choice

from django.http import HttpResponse
from django.urls import path
from django.db import connection

from django_redis import get_redis_connection


# Rate-limiting middleware


def rate_limit(get_response):
    # Configuration

    def limit_request(request):
        remote_ip = request.META['REMOTE_ADDR']
        con = get_redis_connection()
        minute = datetime.now().minute
        key = f'rate_limit:{remote_ip}:{minute}'

        # MULTI
        # INCR key
        # EXPIRE key 59
        # EXEC

        with con.pipeline() as pipe:
            pipe.multi()
            pipe.incr(key)
            pipe.expire(key, 59)
            hits, _ = pipe.execute()

        if hits > RATE_LIMIT:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429
            return HttpResponse('Too many requests', status=429)
        response = get_response(request)
        return response

    return limit_request


RATE_LIMIT = 5
ROOT_URLCONF = __name__
DEBUG = True
SECRET_KEY = 'secret'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379'
    }

}
MIDDLEWARE = [
    'zen.rate_limit',
]

text = ''.join(this.d.get(c, c) for c in this.s)
title, _, *quotes = text.splitlines()


template = """
<!DOCTYPE html>
<html>
<head>
 <title>{title}</title>
</head>
<body>
 <h1>{quote}</h1>
</body>
</html>
"""


def hello(request):
    return HttpResponse(template.format(title=title, quote=choice(quotes)))


urlpatterns = [
    path('', hello)
]


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line()
