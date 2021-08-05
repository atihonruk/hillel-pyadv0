from celery import shared_task

from .models import Download

# import requests


# app = Celery('tasks',
#             broker='redis://localhost/1',
#             backend='redis://localhost/2')


@shared_task
def fac(n):
    for x in range(1, n):
        n *= x
    return n


@shared_task
def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


@shared_task
def loader():
    pass
