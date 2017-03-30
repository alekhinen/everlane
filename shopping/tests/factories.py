import factory

from django.contrib.auth.models import User
from shopping.models import Product, ShoppingCart, PurchaseHistory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
    username = factory.Sequence(lambda n: 'person{0}'.format(n))


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    title = "Test Product"
    price = 20.0
    available_inventory = 10


class ShoppingCartFactory(factory.DjangoModelFactory):
    class Meta:
        model = ShoppingCart

    owner = factory.SubFactory(UserFactory)


class PurchaseHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = PurchaseHistory

    owner = factory.SubFactory(UserFactory)
