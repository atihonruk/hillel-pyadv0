import this

from django.http import HttpResponseNotFound
from django.shortcuts import render


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
        query_string = request.POST.get('query_string')
        if query_string:
            result = [(i, q) for i, q in enumerate(quotes)
                      if query_string.lower() in q.lower()]
            ctx['query_string'] = query_string
            ctx['result'] = result
    return render(request, 'search.html', ctx)
