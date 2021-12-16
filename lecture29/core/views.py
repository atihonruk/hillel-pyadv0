from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Q
from django.db.models.functions import Extract, Now
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View, TemplateView, RedirectView, DetailView, ListView, CreateView
from django.views.generic.detail import SingleObjectMixin

from .models import Author, Book
from .autocomplete import get_completion

# @login_required(login_url='')
def index(request):
    return render(request, 'index.html', {})


class Index(View):
    def post(self, *args, **kwargs):
        return HttpResponse('Hello, worlds')

    def get(self, *args, **kwargs):
        return HttpResponse('Hello, GET')


class LocalizationMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs) #!
        ctx['greeting'] = 'Привет'
        return ctx


class Index2(LocalizationMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs) #!
        ctx['name'] = 'Django'
        return ctx

    
class RedirectKey(RedirectView):
    
    def get(self, request, **kwargs):
        self.key = kwargs.get('key')
        return super().get(request, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        # url = Url.object.get(self.key)
        url = 'http://python.org'
        return url


class AuthorDetails(DetailView):
    model = Author
    template_name = 'author_details.html'


class AuthorList(ListView):
    model = Author
    paginate_by = 5
    template_name = 'author_list.html'


class CreateAuthor(CreateView):
    model = Author
    fields = ('name', 'email')
    template_name = 'create_author.html'


class BookDetails(DetailView):
    model = Book
    template_name = 'book_details.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.incr_view_count()
        return obj

# (SingleObjectMixin, MultipleObjectMixin, TemplateView)
# (MultipleObjectMixin, DetailView)
class AuthorBooksView(SingleObjectMixin, ListView):
    template_name = 'author_books.html'

    def get_queryset(self):
        return self.object.book_set.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Author.objects.all())
        return super().get(request, *args, **kwargs)

from pprint import pprint

class BookList(ListView):
    model = Book
    paginate_by = 10
    template_name = 'book_list.html'

    # predefined filters with the Q objects
    # cheap [0, 100], exp > 300

    FILTERS = {
        # by price
        'cheap': Q(price__lte=100),
        'expensive': Q(price__gt=10),
        # by published date
        'upcoming': Q(published_at__gt=Now()),
        # by stock availability
        'in_stock': Q(stock__gt=0),
    }

    def get_queryset(self):
        # простые фильтры: GET параметры из строки запроса
        params = {k + '__in': list(v) for k, v in self.request.GET.lists()}

        # именованные фильтры из словаря FILTERS
        filters = self.kwargs.get('filters', '').split('-')
        clauses = [self.FILTERS[f] for f in filters if f in self.FILTERS]
        qs = Book.objects.filter(*clauses, **params)
        return qs

    
def autocomplete_book(request):
    term = request.GET.get('term', None)
    result = []
    if term:
        ids = get_completion(Book, 'title', term.lower())
        if ids:
            result = [{
                'id': obj.id,
                'title': obj.title
            } for obj in Book.objects.filter(id__in=ids)]  # where id in (1, 2, 3)

    return JsonResponse(result, safe=False)
