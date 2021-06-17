from django.db import models

# Create your models here.


class Author(models.Model):
    # id =  AutoField()
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)


class Book(models.Model):
    # id = AutoField()
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=30, unique=True)
    authors = models.ManyToManyField(Author)

    class Meta:
        pass


class Account(models.Model):
    amount = models.IntegerField()


# class BooksAuthors(models.Model):
#     author = models.ForeignKey(Author)
#     book = models.ForeignKey(Book)
