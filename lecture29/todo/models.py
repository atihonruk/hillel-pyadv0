from django.db import models

from django.conf import settings


class Todo(models.Model):
    TODO, DONE, CANCELED = range(3)
    
    STATUS_CHOICES = [
        (TODO, 'Todo'),
        (DONE, 'Done'),
        (CANCELED, 'Canceled'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=TODO)
