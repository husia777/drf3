import pytest

@pytest.mark.django_db
@pytest.fixture
def jwt_token(client, django_user_model):
    username = "12345"
    password = "123qwe"
    django_user_model.objects.create_user(
    username=username,
    password = password,
    role = "moderator",
    age = 23
    )
    response = client.post('/token/',
                {"username":username,
                "password":password},
                format="json")
    return response.data['access']