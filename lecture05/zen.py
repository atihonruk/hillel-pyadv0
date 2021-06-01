import this

from django.core.management import execute_from_command_line
from django.http import HttpResponseNotFound
from django.urls import path

from django.shortcuts import render


DEBUG = True
ROOT_URLCONF = __name__
SECRET_KEY = 'secret'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [''],
    }
]

text = ''.join(this.d.get(c, c) for c in this.s)
title, _, *quotes = text.splitlines()


def index(request):
    return render(request, 'index.html', {'quotes': quotes})


def handler(request, index):
    if index < len(quotes):
        return render(request, 'zen.html', {'quote': quotes[index]})
    else:
        return HttpResponseNotFound(f'Quote {index} is not found')


def search(request):
    ctx = {}
    if request.POST:
        query_string = request.POST.get('query_string', '')
        result = [(i, q) for i, q in enumerate(quotes) if query_string.lower() in q.lower()]
        ctx['query_string'] = query_string
        ctx['result'] = result
    return render(request, 'search.html', ctx)


urlpatterns = [
    path('quotes/search', search, name='search'),
    path('quotes', index, name='index'),
    path('quotes/<int:index>', handler, name='quote'),

]


if __name__ == '__main__':
    execute_from_command_line()
