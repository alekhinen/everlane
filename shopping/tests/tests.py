from django.test import TestCase
from factories import UserFactory, ProductFactory, ShoppingCartFactory, PurchaseHistoryFactory

# Create your tests here.

class ShoppingCartTest(TestCase):
    def setUp(self):
        # generate some stuff
        ProductFactory(title="black shirt", price=15.00, available_inventory=200)
        ProductFactory(title="velvet button down", price=150.00, available_inventory=2)

    def test_add_product(self):
        shopping_cart = ShoppingCartFactory()
        # a shopping cart should start off empty
        self.assertEqual(len(shopping_cart.products.all()), 0)
