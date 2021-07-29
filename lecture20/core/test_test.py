import pytest

class Client:
    pass


@pytest.fixture
def client():
    # setup
    yield Client()
    # tear down



def test_test1(client):
    assert 1 == True


def test_test2(client):
    assert 0 == False
