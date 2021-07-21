from random import randint
from django.db import models
from django.utils.baseconv import base56

from django.conf import settings

MIN_KEY, MAX_KEY = 80106440, 550731775


def random_key():
    return base56.encode(randint(MIN_KEY, MAX_KEY))


class Url(models.Model):
    key = models.SlugField()
    url = models.URLField()
    user = settings.AUTH_USER_MODEL

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = random_key()
        super().save(*args, **kwargs)
