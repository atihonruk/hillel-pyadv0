from urllib.parse import urlparse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import Url


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ('url',)


def create_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_bound and form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'register.html', {'form': form})


def redirect_key(request, key):
    try:
        url = Url.objects.get(key=key).url
    except Model.DoesNotExists:
        url = reverse('index')
    return redirect(to=url)


@login_required
def index(request):
    ctx = {}
    form = UrlForm(request.POST or None)
    if form.is_bound and form.is_valid():
        obj = form.save()
        ctx['key'] = obj.key
        form = UrlForm()
    ctx['form'] = form
    return render(request, 'index.html', ctx)
