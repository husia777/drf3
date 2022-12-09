import pytest
from tests.factories import AdsFactory
from ads.serializers import AdsListSerializer
@pytest.mark.django_db
def test_ads_list(client):
    ads = AdsFactory.create_batch(5)
    data = AdsListSerializer(ads, many=True).data
    r = client.get(f'/ad/')
    assert r.status_code == 200
    assert r.data == data