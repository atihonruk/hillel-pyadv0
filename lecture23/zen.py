import this

from random import choice

from django.http import HttpResponse
from django.urls import path
from django.db import connection

from django_redis import get_redis_connection


ROOT_URLCONF = __name__
DEBUG = True
SECRET_KEY = 'secret'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379'
    }

}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'HOST': 'db',
        'USER': 'django_user',
        'PASSWORD': 'postgres',
        'PORT': 5432,
    }
}


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
 <p>Hits: {hits}</p>
 <p>DB Hits: {db_hits}</p>
</body>
</html>
"""


def hello(request):
    with connection.cursor() as dbcur:
        dbcur.execute('create table if not exists hits(key char(30), count bigint)')
        dbcur.execute('insert into hits values(%s, %s)', ['zen:index:view_count', 1])
    
    con = get_redis_connection()
    hits = con.incr('zen:index:view_count')

    with connection.cursor() as dbcur:
        dbcur.execute('select count from hits')
        db_hits = dbcur.fetchone()

    return HttpResponse(template.format(title=title, quote=choice(quotes), hits=hits, db_hits=db_hits))


urlpatterns = [
    path('', hello)
]


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line()
