import factory
from factory.django import DjangoModelFactory

from ads.models import Ads, Users, Compilation, Locations, Category


class LocationsFactory(DjangoModelFactory):
    class Meta:
        model = Locations

    name = 'Тестовая локация'


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = 'Котики'
    slug = factory.Sequence(lambda n: 'user%d' % n)


class UsersFactory(DjangoModelFactory):
    class Meta:
        model = Users

    first_name = "Петр"
    last_name = "1"
    username = factory.Sequence(lambda n: 'user%d' % n)
    password = "1"
    role = "user"
    age = "22"
    email = factory.Sequence(lambda n: 'user%d' % n)

    @factory.post_generation
    def location(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for loc in extracted:
                self.location.add(loc)


class CompilationFactory(DjangoModelFactory):
    class Meta:
        model = Compilation

    name = 'test'
    owner = factory.SubFactory(UsersFactory)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for item in extracted:
                self.items.add(item)


class AdsFactory(DjangoModelFactory):
    class Meta:
        model = Ads

    name = "ерывеарарарапр"
    author = factory.SubFactory(UsersFactory)
    price = 9
    description = ""
    category = factory.SubFactory(CategoryFactory)
    is_published = False
