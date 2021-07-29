from django.db import models
from django_redis import get_redis_connection

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def get_absolute_url(self):
        return '/author/' + str(self.pk)

    def __str__(self):
        return f'{self.name} <{self.email}>'
        

class Book(models.Model):
    CATEGORIES = [
        (1, 'fiction'),
        (2, 'non-fiction'),
    ]

    slug = models.SlugField()
    isbn = models.CharField(unique=True, max_length=13)
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    category = models.IntegerField(choices=CATEGORIES)
    cover = models.ImageField(upload_to='covers', blank=True, null=True)

    def incr_view_count(self):
        key = f'{self._meta.db_table}:{self.pk}'
        con = get_redis_connection()
        con.incr(key)
        print(con, key)

    def view_count(self):
        key = f'{self._meta.db_table}:{self.pk}'
        con = get_redis_connection()
        return int(con.get(key))
        
    def __str__(self):
        return f'{self.pk}: {self.title}'
