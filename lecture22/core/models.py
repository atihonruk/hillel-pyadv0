from django.db import models

class Download(models.Model):
    url = models.URLField()
    tmp = models.FileField()


class Log(models.Model):
    download = models.ForeignKey(Download, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
