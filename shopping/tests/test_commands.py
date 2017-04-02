from django.test import TestCase
from factories import UserFactory, ProductFactory, ShoppingCartFactory, PurchaseHistoryFactory
from django.core.management import call_command
from StringIO import StringIO

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

    def test_remove_from_cart(self):
        self.shopping_cart.add_product(self.button_down.pk, 1)
        call_command("remove_from_cart", str(self.user.pk), str(self.button_down.pk))
        self.assertEqual(len(self.shopping_cart.products.all()), 0)

    def test_purchase(self):
        self.shopping_cart.add_product(self.button_down.pk, 1)
        self.shopping_cart.add_product(self.shirt.pk, 3)
        call_command("purchase", str(self.user.pk))
        self.assertEqual(len(self.user.purchase_history.all()), 1)

    def test_view_purchase_history(self):
        self.shopping_cart.add_product(self.button_down.pk, 2)
        self.shopping_cart.add_product(self.shirt.pk, 1)
        self.shopping_cart.purchase()
        out = StringIO()
        call_command("view_purchase_history", str(self.user.pk), stdout=out)
        print out.getvalue()

