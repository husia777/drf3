import pytest

from ads.serializers import  CompilationCreateSerializer
from tests.factories import CompilationFactory

@pytest.mark.django_db
def test_create_compilation(client, jwt_token):
    compilation = CompilationFactory.create()
    data = CompilationCreateSerializer(compilation).data


    r = client.post('/compilation/create/',
                    data,
                    content_type='application/json'
                    , HTTP_AUTHORIZATION='Bearer ' + jwt_token
                    )
    assert r.status_code  == 201
    assert r.data == data