from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def get_absolute_url(self):
        return '/author/' + str(self.pk)


class Book(models.Model):
    slug = models.SlugField()
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=100)
