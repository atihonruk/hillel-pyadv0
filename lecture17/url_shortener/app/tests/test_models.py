import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


def test_generated_key():
    obj = mixer.blend('app.Url')
    assert len(obj.key) == 5


def test_has_user():
    user = mixer.blend('auth.user', username='Tom Sawyer') # , commit=False)
    
