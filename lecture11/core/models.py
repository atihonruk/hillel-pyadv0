from random import randint

from django.db import models
from django.utils.baseconv import base56

MIN_KEY, MAX_KEY = 80106440, 550731775


class Url(models.Model):
    key = models.SlugField(unique=True)
    url = models.URLField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = base56.encode(randint(MIN_KEY, MAX_KEY))
        super().save(*args, **kwargs)
