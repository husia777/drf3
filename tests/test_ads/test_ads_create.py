import pytest

from ads.serializers import AdsCreateSerializer
from tests.factories import  AdsFactory


@pytest.mark.django_db
def test_create(client):
    data = AdsFactory.create()
    data = AdsCreateSerializer(data).data
    expected_response = {
        "name": "ерывеарарарапр",
        "author": "Петр",
        "price": 9,
        "description": "",
        "category": "Котики",
        "is_published": False}

    r = client.post('/ad/create/', data, format='json')
    assert r.status_code == 201
    assert r.data == expected_response
