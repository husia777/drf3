import pytest

from ads.serializers import AdsCreateSerializer, AdsDetailSerializer
from tests.factories import AdsFactory


@pytest.mark.django_db
def test_detail(client, jwt_token, ads):
    ads = AdsFactory.create()
    print(ads)
    data = AdsDetailSerializer(ads).data
    print(data)
    expected_response = {
        "id": ads.id,
        "name": "ерывеарарарапр",
        "author": "Петр",
        "price": 9,
        "description": "",
        "category": "Котики",
        "is_published": False}

    r = client.get(f'/ad/{ads.id}/',
                   content_type='application/json'
                   , HTTP_AUTHORIZATION='Bearer ' + jwt_token
                   )
    assert r.status_code == 200
    assert r.data == expected_response
