from django.test import TestCase
from factories import UserFactory, ProductFactory, ShoppingCartFactory, PurchaseHistoryFactory
from shopping.management.commands import add_to_cart, purchase, remove_from_cart, view_purchase_history
from django.core.management import call_command

class CommandTestCase(TestCase):
    def setUp(self):
        # generate some products
        self.shirt = ProductFactory(title="black shirt", price=15.00, available_inventory=200)
        self.button_down = ProductFactory(title="velvet button down", price=150.00, available_inventory=2)
        # generate a user
        self.user = UserFactory()
        # generate a shopping cart
        self.shopping_cart = ShoppingCartFactory(owner=self.user)

    def test_add_to_cart(self):
        # you should be able to add to a user's cart from the command line.
        call_command("add_to_cart",'{0}'.format(self.user.pk), '{0}'.format(self.shirt.pk), '5')
        products = self.shopping_cart.products.all()
        self.assertEqual(len(products), 1)
