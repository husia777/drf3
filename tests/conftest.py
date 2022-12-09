from pytest_factoryboy import register

from tests.factories import AdsFactory, CompilationFactory, LocationsFactory, CategoryFactory, UsersFactory
pytest_plugins = "tests.fixtures"

# Factories
register(AdsFactory, _name='ads')
register(CompilationFactory, _name='compilation')
register(LocationsFactory, _name='locations')
register(CategoryFactory, _name='category')
register(UsersFactory, _name='users')