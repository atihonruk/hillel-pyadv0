import sys
import this

from django.core.management import execute_from_command_line
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import path


ROOT_URLCONF = __name__
DEBUG = True
SECRET_KEY = 'secret'


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


def handler(request, index):
    if index < len(quotes):
        return HttpResponse(quotes[index])
    else:
        return HttpResponseNotFound(f'Quote {index} is not found')


urlpatterns = [
    path('quote/<int:index>', handler),
]


execute_from_command_line(sys.argv)
