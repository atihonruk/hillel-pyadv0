from unittest.mock import patch

import pytest

pytestmark = pytest.mark.django_db


# urlpatterns, middleware
def test_index_key_client(client):
    res = client.get('/')
    res.status_code == 200


test_url = 'https://python.org'
test_key = 'dummy'


def test_redirect(client):
    with patch('app.models.random_key', lambda: test_key):
        response = client.post('/', {'url': test_url})
        assert response.status_code == 200
        assert test_key in response.content.decode()

        # /asdlj -> http://python.org
        response = client.get('/' + test_key)
        assert response.status_code == 302
        assert response.url == test_url


def test_index_key_rf(rf): # RequestFactory
    pass
    
