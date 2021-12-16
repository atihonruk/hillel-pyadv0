from django.test import TestCase

class Client:
    pass


def client():
    yield Client()



def test_test1(client):
    assert 1 == True


def test_test2(client):
    assert 0 == False
