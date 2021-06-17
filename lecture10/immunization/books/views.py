from django.shortcuts import render, redirect

from django import forms

from books.models import Author, Book


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()

    # def clean_name(self):
    #    return self.upper()

    # def clean_email(self):
    #    return val.lower()


class AuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'email']


def create(request):
    form = AuthorModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'index.html', {'form': form})


def edit(request, pk):
    a = Author.objects.get(pk=pk)
    form = AuthorModelForm(request.POST or None, instance=a)
    if form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'index.html', {'form': form})
